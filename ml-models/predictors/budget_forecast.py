"""
Budget Forecast ML Model and FastAPI Router
- Provides /predict and /train endpoints for budget forecasting
- Can be imported as a FastAPI router or run as a script for CLI testing
"""
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib
import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, conlist
from typing import List, Annotated

MODEL_PATH = "budget_forecast_model.pkl"

class BudgetForecaster:
    def __init__(self):
        self.model = LinearRegression()
        if os.path.exists(MODEL_PATH):
            self.model = joblib.load(MODEL_PATH)

    def fit(self, X, y):
        self.model.fit(X, y)
        joblib.dump(self.model, MODEL_PATH)

    def predict(self, X):
        X = np.array(X)
        if X.ndim == 1:
            X = X.reshape(1, -1)
        return self.model.predict(X)

# --- FastAPI Router for ML ---
router = APIRouter()

class PredictRequest(BaseModel):
    features: List[Annotated[list[float], conlist(float, min_length=2)]]  # Example: [[1.0, 2.0], [2.0, 3.0]]

class PredictResponse(BaseModel):
    predictions: List[float]

class TrainRequest(BaseModel):
    features: List[Annotated[list[float], conlist(float, min_length=2)]]
    targets: List[float]

@router.post("/predict", response_model=PredictResponse, tags=["ML"])
def predict_budget(data: PredictRequest):
    """Predict budget for given features (batch or single)."""
    try:
        forecaster = BudgetForecaster()
        preds = forecaster.predict(data.features)
        return {"predictions": preds.tolist()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/train", tags=["ML"])
def train_budget(data: TrainRequest):
    """Train the model with features and targets."""
    try:
        forecaster = BudgetForecaster()
        forecaster.fit(data.features, data.targets)
        return {"message": "Model trained successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def fit_example():
    # Example: Fit on dummy data
    X = np.array([[1, 2], [2, 3], [3, 4]])
    y = np.array([100, 200, 300])
    forecaster = BudgetForecaster()
    forecaster.fit(X, y)
    print("Model trained and saved.")

def predict_example():
    # Example: Predict on new data
    forecaster = BudgetForecaster()
    print("Single prediction:", forecaster.predict([4, 5]))
    print("Batch prediction:", forecaster.predict([[4, 5], [5, 6]]))

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "fit":
        fit_example()
    else:
        predict_example()