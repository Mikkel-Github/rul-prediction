import pandas as pd


def preprocess_data(df: pd.DataFrame, sampling_interval: int = 500):
    print("Preprocessing the data...")
    df.sort_values(by=["machine_id", "active_time"], inplace=True)
    print("Sorted the dataset")

    rows = []

    print("Preprocessing for each machine...")
    for machine_id, machine_df in df.groupby("machine_id"):
        machine_df = machine_df.reset_index(drop=True)
        machine_type = machine_df["machine_type"].iloc[0]

        known_components = (
            machine_df[
                machine_df["event_type"].isin(["Failure", "Preemptive Replacement"])
            ]["fault_type"]
            .dropna()
            .unique()
            .tolist()
        )

        install_time = {comp: 0 for comp in known_components}
        failure_counts = {comp: 0 for comp in known_components}
        lifecycle_ids = {comp: 0 for comp in known_components}
        service_history = []

        for idx, row in machine_df.iterrows():
            time = row["active_time"]
            event_type = row["event_type"]
            component = row["fault_type"] if pd.notna(row["fault_type"]) else None

            if event_type in ["Failure", "Preemptive Replacement"]:
                if component:
                    start = install_time[component]
                    end = time
                    curr_lifecycle = lifecycle_ids[component]

                    # NOTE: removed the interpolating samples as they just confused the models more.

                    # for t in range(start + sampling_interval, end, sampling_interval):
                    #     num_services = len(
                    #         [s for s in service_history if start < s < t]
                    #     )
                    #     last_service = max(
                    #         [s for s in service_history if start < s < t], default=start
                    #     )
                    #     rows.append(
                    #         {
                    #             "machine_id": machine_id,
                    #             "machine_type": machine_type,
                    #             "component": component,
                    #             "active_time": t,
                    #             "component_age": t - start,
                    #             "prev_failures": failure_counts[component],
                    #             "num_services_since_install": num_services,
                    #             "time_since_last_service": t - last_service,
                    #             "RUL": end - t,
                    #             "event_type_encoded": 0,
                    #             "lifecycle_id": curr_lifecycle,
                    #             "is_failure": 0,
                    #         }
                    #     )

                    num_services = len([s for s in service_history if start < s < end])
                    last_service = max(
                        [s for s in service_history if start < s < end], default=start
                    )
                    rows.append(
                        {
                            "machine_id": machine_id,
                            "machine_type": machine_type,
                            "component": component,
                            "active_time": end,
                            "component_age": end - start,
                            "prev_failures": failure_counts[component],
                            "num_services_since_install": num_services,
                            "time_since_last_service": end - last_service,
                            "RUL": 0,
                            "event_type_encoded": 2,
                            "lifecycle_id": curr_lifecycle,
                            "is_failure": 1,
                        }
                    )

                    failure_counts[component] += 1
                    lifecycle_ids[component] += 1
                    install_time[component] = time

                    rows.append(
                        {
                            "machine_id": machine_id,
                            "machine_type": machine_type,
                            "component": component,
                            "active_time": time,
                            "component_age": 0,
                            "prev_failures": failure_counts[component],
                            "num_services_since_install": 0,
                            "time_since_last_service": 0,
                            "RUL": None,
                            "event_type_encoded": 0,
                            "lifecycle_id": lifecycle_ids[component],
                            "is_failure": 0,
                        }
                    )

            elif event_type == "Service":
                service_history.append(time)
                for component in known_components:
                    if install_time[component] >= time:
                        continue

                    future_failures = machine_df[
                        (machine_df["active_time"] > time)
                        & (machine_df["fault_type"] == component)
                        & (
                            machine_df["event_type"].isin(
                                ["Failure", "Preemptive Replacement"]
                            )
                        )
                    ]
                    rul = (
                        future_failures["active_time"].iloc[0] - time
                        if not future_failures.empty
                        else None
                    )

                    num_services = len(
                        [
                            s
                            for s in service_history
                            if install_time[component] < s < time
                        ]
                    )
                    last_service = max(
                        [
                            s
                            for s in service_history
                            if install_time[component] < s < time
                        ],
                        default=install_time[component],
                    )

                    rows.append(
                        {
                            "machine_id": machine_id,
                            "machine_type": machine_type,
                            "component": component,
                            "active_time": time,
                            "component_age": time - install_time[component],
                            "prev_failures": failure_counts[component],
                            "num_services_since_install": num_services,
                            "time_since_last_service": time - last_service,
                            "RUL": rul,
                            "event_type_encoded": 1,
                            "lifecycle_id": lifecycle_ids[component],
                            "is_failure": 0,
                        }
                    )
    print("Done grouping by machines...")
    feature_df = pd.DataFrame(rows)
    feature_df = feature_df.dropna(subset=["RUL"])

    print("Done preprocessing")

    return feature_df


def preprocess_single_machine_latest_entry(
    df: pd.DataFrame, machine_id: str
) -> pd.DataFrame:
    print(f"Preprocessing for prediction on machine {machine_id}...")

    machine_df = df[df["machine_id"] == machine_id].sort_values(by="active_time")
    if machine_df.empty:
        raise ValueError(f"No data found for machine {machine_id}")

    machine_type = machine_df["machine_type"].iloc[0]

    known_components = (
        machine_df[
            machine_df["event_type"].isin(["Failure", "Preemptive Replacement"])
        ]["fault_type"]
        .dropna()
        .unique()
        .tolist()
    )

    rows = []

    for component in known_components:
        # first find all installments
        # an installemnt is when a component has failed, a new one is installed
        installs = machine_df[
            (machine_df["fault_type"] == component)
            & (machine_df["event_type"].isin(["Failure", "Preemptive Replacement"]))
        ]
        if installs.empty:
            continue

        latest_install_time = installs["active_time"].max()
        lifecycle_id = installs.shape[0]
        prev_failures = lifecycle_id

        events_after_install = machine_df[
            machine_df["active_time"] > latest_install_time
        ]

        services_after_install = events_after_install[
            events_after_install["event_type"] == "Service"
        ]
        num_services = len(services_after_install)

        last_service_time = (
            services_after_install["active_time"].max()
            if not services_after_install.empty
            else latest_install_time
        )

        last_event_time = (
            events_after_install["active_time"].max()
            if not events_after_install.empty
            else latest_install_time
        )

        row = {
            "machine_id": machine_id,
            "machine_type": machine_type,
            "component": component,
            "active_time": last_event_time,
            "component_age": last_event_time - latest_install_time,
            "prev_failures": prev_failures,
            "num_services_since_install": num_services,
            "time_since_last_service": last_event_time - last_service_time,
            "event_type_encoded": 0,
            "lifecycle_id": lifecycle_id,
            "is_failure": 0,
        }
        print(row)
        rows.append(row)

    return pd.DataFrame(rows)


df = pd.read_csv("./synthetic_failure_and_service_data.csv")
df.sort_values(by=["machine_id", "active_time"], inplace=True)
feature_df = preprocess_data(df)
feature_df.to_csv("dataset_settings_4.csv", index=False)
