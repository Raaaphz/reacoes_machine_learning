class PredictionRepository:
    def __init__(self, model):
        self.model = model
    
    def predict(self, text):
        return self.model.predict([text])[0]