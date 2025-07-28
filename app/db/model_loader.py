import spacy

class ModeLoader:
    def __init__(self, model_path):
        self.model_path = model_path
    
    def get_model(self):
        return spacy.load(self.model_path)