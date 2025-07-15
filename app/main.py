from fastapi import FastAPI, HTTPException
import pandas as pd
from core.config import app
from db.model_loader import ModelLoader
from domain.input_models import TextInput
from repositories.prediction_repository import PredictionRepository
from services.prediction_service import PredictionService
import uvicorn
from pydantic import BaseModel

dataset=pd.read_csv("/models/data.csv")
