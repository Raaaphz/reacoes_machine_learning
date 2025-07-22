import string
import pandas as pd
import uvicorn
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from core.config import app
from db.model_loader import ModelLoader
from domain.input_models import TextInput
from repositories.prediction_repository import PredictionRepository
from services.prediction_service import PredictionService
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

dataset=pd.read_csv("C:/Users/rapha/VSCodeProjects/tcc_machine_learning/app/models/data.csv", encoding='utf-8')

#processamento dos dados
pontuacoes = string.punctuation
pln = spacy.load('en_core_web_sm')
stop_words = STOP_WORDS

def preprocessamento(Tweets):
    Tweets = Tweets.lower()
    documento = pln(Tweets)
    lista = []
    for token in documento:
        lista.append(token.lemma_)
        
    lista = [palavra for palavra in lista if palavra not in stop_words and palavra not in pontuacoes]
    
    lista = ' '.join([str(elemento)for elemento in lista if not elemento.isdigit()])
    return lista

#pre processamento da base de dados
dataset['Tweets'] = dataset['Tweets'].apply(preprocessamento)

dataset_final = []
i = 0
for Tweets, Feeling in zip(dataset['Tweets'], dataset['Feeling']):
    if Feeling =='happy':
        dic = ({'HAPPY': True, 'SAD': False, 'ANGRY': False, 'FEAR': False, 'DISGUST': False})
    elif Feeling =='sad':
        dic = ({'HAPPY': False, 'SAD': True, 'ANGRY': False, 'FEAR': False, 'DISGUST': False})
    elif Feeling == 'angry':
        dic = ({'HAPPY': False, 'SAD': False, 'ANGRY': True, 'FEAR': False, 'DISGUST': False})
    elif Feeling == 'fear':
        dic = ({'HAPPY': False, 'SAD': False, 'ANGRY': False, 'FEAR': True, 'DISGUST': False})
    elif Feeling == 'disgust':
        dic = ({'HAPPY': False, 'SAD': False, 'ANGRY': False, 'FEAR': False, 'DISGUST': True})
    dataset_final.append([Tweets, dic.copy()])

#rodar o server
if __name__ =="__main__":
    uvicorn.run("main:app", host="0.0.0.0",port=3636, reload=True)