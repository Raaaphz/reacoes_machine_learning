class PredictionService:
    def __init__(self, prediction_repository):
        self.prediction_repository = prediction_repository
        
    def make_prediction(self, text: str):
        return self.prediction_repository.predict(text)