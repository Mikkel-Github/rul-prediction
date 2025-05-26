import pandas as pd


def assess_risk(prediction_results, machines):
    # add every predicted rul to the records, this is from the prediction.py script
    records = []
    for item in prediction_results:
        machine_id = item["machine_id"]
        for res in item["results"]:
            records.append(
                {
                    "machine_id": machine_id,
                    "component": res["component"],
                    "component_age": res["component_age"],
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

    def compute_risk(row):
        if row["predicted_rul"] is None:
            return "Unknown"
        ratio = row["predicted_rul"] / (row["predicted_rul"] + row["component_age"])
        if ratio <= 0.2:
            return "High Risk"
        elif ratio <= 0.4:
            return "Medium Risk"
        else:
            return "Low Risk"

    prediction_df["risk_level"] = prediction_df.apply(compute_risk, axis=1)

    grouped_output = []
    for machine_id, group in prediction_df.groupby("machine_id"):
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
