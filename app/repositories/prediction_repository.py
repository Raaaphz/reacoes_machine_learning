class PredictionRepository:
    def __init__(self, model):
        self.model = model
    
    def predict(self, text):
        doc = self.model(text)
        
        if hasattr(doc, "cats") and doc.cats:
            return max (doc.cats, key=doc.cats.get)
        return "unknown"
       # return self.model.predict([text])[0]