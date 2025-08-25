import uvicorn
from core.config import app
from db.model_loader import ModelLoader
from domain.input_models import TextInput
from repositories.prediction_repository import PredictionRepository
from services.prediction_service import PredictionService
from fastapi import HTTPException
from pydantic import BaseModel

#Inicializar modelo
model_loader = ModelLoader('app/models/modelo_reacoes')
model = model_loader.get_model()

#cira instancia do servico de predição
prediction_repository = PredictionRepository(model)
prediction_service = PredictionService(prediction_repository)

class TextInput(BaseModel):
    text:str
    
@app.post("/api/prediction")
async def predict(data: TextInput):
    
    try:
        prediction = prediction_service.make_prediction(data.text)
        return {"prediction": prediction}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
            
#rodar o server
if __name__ =="__main__":
    uvicorn.run("main:app", host="0.0.0.0",port=3636, reload=True)