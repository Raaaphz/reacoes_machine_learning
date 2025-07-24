import string
import pandas as pd
import uvicorn
import spacy
import re
import random
from spacy.lang.en.stop_words import STOP_WORDS
from core.config import app
from db.model_loader import ModelLoader
from domain.input_models import TextInput
from repositories.prediction_repository import PredictionRepository
from services.prediction_service import PredictionService
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

            
#rodar o server
if __name__ =="__main__":
    uvicorn.run("main:app", host="0.0.0.0",port=3636, reload=True)