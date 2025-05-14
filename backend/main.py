import json

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from scripts.risk_signal import assess_risk
from services.prediction import predict_rul, predict_rul_all_machines
from services.training import train_model

app = FastAPI()


class AllPredictionRequest(BaseModel):
    machines: list[dict]
    events: list[dict]


class PredictionRequest(BaseModel):
    machine_id: str
    machines: list[dict]
    events: list[dict]


class TrainRequest(BaseModel):
    machines: list[dict]
    events: list[dict]


@app.post("/train")
async def train(train_request: TrainRequest):
    try:
        print("Initiating training...")
        print(train_request.machines)
        train_model(train_request.machines, train_request.events)
        return {"status": "Model trained"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict-all")
async def predictAll(prediction_request: AllPredictionRequest):
    try:
        print("Initiating prediction for all machines...")
        predictions = predict_rul_all_machines(
            prediction_request.machines, prediction_request.events
        )
        risk_df = assess_risk(predictions, prediction_request.machines)
        print(risk_df)
        return risk_df
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict")
async def predict(prediction_request: PredictionRequest):
    try:
        print("Initiating prediction...")
        predictions = predict_rul(
            prediction_request.machine_id,
            prediction_request.machines,
            prediction_request.events,
        )
        risk_df = assess_risk(predictions, prediction_request.machines)
        print(risk_df)
        return risk_df
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
