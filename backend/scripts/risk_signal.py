import pandas as pd


def assess_risk(
    prediction_results, machines, avg_lifespan_path="data/average_lifespan.csv"
):
    # add every predicted rul to the records, this is from the prediction.py script
    records = []
    for item in prediction_results:
        machine_id = item["machine_id"]
        for res in item["results"]:
            records.append(
                {
                    "machine_id": machine_id,
                    "component": res["component"],
                    "predicted_rul": res["predicted_rul"],
                }
            )

    prediction_df = pd.DataFrame(records)

    # join the machines onto the predictions
    df_machines = pd.DataFrame(machines)
    prediction_df = pd.merge(
        prediction_df,
        df_machines[["machine_id", "machine_type"]],
        on="machine_id",
        how="left",
    )

    # then get the average life spans from the average_lifespan.csv
    avg_lifespans = pd.read_csv(avg_lifespan_path)
    merged = pd.merge(
        prediction_df, avg_lifespans, on=["machine_type", "component"], how="left"
    )

    # then output a risk based on how long the component has left out of its full life
    def compute_risk(row):
        if pd.isna(row["avg_lifespan"]) or row["predicted_rul"] is None:
            return "Unknown"
        ratio = row["predicted_rul"] / row["avg_lifespan"]
        if ratio <= 0.15:
            return "High Risk"
        elif ratio <= 0.35:
            return "Medium Risk"
        else:
            return "Low Risk"

    merged["risk_level"] = merged.apply(compute_risk, axis=1)

    grouped_output = []
    for machine_id, group in merged.groupby("machine_id"):
        results = []
        for _, row in group.iterrows():
            results.append(
                {
                    "component": row["component"],
                    "predicted_rul": float(row["predicted_rul"]),
                    "risk_level": row["risk_level"],
                }
            )
        grouped_output.append({"machine_id": str(machine_id), "results": results})

    return {"predictions": grouped_output}
