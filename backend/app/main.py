from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import expenses
import importlib.util
import os

# Dynamically import budget_forecast from ml-models/predictors
ml_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../ml-models/predictors/budget_forecast.py'))
spec = importlib.util.spec_from_file_location('budget_forecast', ml_path)
budget_forecast = importlib.util.module_from_spec(spec)
spec.loader.exec_module(budget_forecast)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(expenses.router, prefix="/api/expenses")
app.include_router(budget_forecast.router, prefix="/api/ml")

@app.get('/')
def read_root():
    return {'message': 'Welcome to SavvySpend Backend'}