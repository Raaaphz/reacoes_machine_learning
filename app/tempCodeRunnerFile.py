import string
import pandas as pd
import spacy
import re
import random
from spacy.lang.en.stop_words import STOP_WORDS
from spacy.training.example import Example

print('Lendo CSV........')
dataset=pd.read_csv("app/models/data.csv", encoding='utf-8')

#processamento dos dados
pontuacoes = string.punctuation
pln = spacy.load('en_core_web_sm')
stop_words = STOP_WORDS

def preprocessamento(Tweets):
    #regex
    #remove "tweet #n"
    Tweets = re.sub(r'Tweet\s+#\d+:','',Tweets)
    
    #remove @usuario
    Tweets = re.sub(r'@\S+','',Tweets)
    
    #remove "tweeted"
    Tweets = re.sub(r'\btweeted\b', '', Tweets, flags=re.IGNORECASE)
    
    #remove links
    Tweets = re.sub(r'https?://\S+', '', Tweets)
    
    #Remove emogis (UNICODE RANGES MAIS COMUNS)
    Tweets = re.sub(r'[\U00010000-\U0010ffff]', '', Tweets)
    
    #remove multiplos espacos
    Tweets = re.sub(r'\s+', ' ', Tweets)
    
    #Remove espacos no inicio/fim
    Tweets = Tweets.strip()
    
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
print('Preprocessamento APLICADO!')

#removendo dados com texto muito curtos ou vazios
dataset = dataset[dataset['Tweets'].str.strip().str.split().str.len() > 2]

dataset_final = []
for Tweets, Feeling in zip(dataset['Tweets'], dataset['Feeling']):
    dic = {'HAPPY': False, 'SAD': False, 'ANGRY': False, 'FEAR': False, 'DISGUST': False, 'SURPRISE': False}
    dic[Feeling.upper()] = True
    dataset_final.append([Tweets, dic.copy()])
    dataset_final.append([Tweets, dic.copy()])

#criar modelo em branco para ingles
model = spacy.blank('en')

textcat = model.add_pipe('textcat')

print(dataset['Feeling'].value_counts())

for categoria in ['HAPPY', 'SAD', 'ANGRY', 'FEAR', 'DISGUST', 'SURPRISE']:
    textcat.add_label(categoria)

model.initialize()

historico = []

for epoca in range(25):
    random.shuffle(dataset_final)
    losses = {}
    for batch in spacy.util.minibatch(dataset_final, 128):
        examples = []
        for Tweets, categorias in batch:
            doc = model.make_doc(Tweets)
            example = Example.from_dict(doc, {"cats": categorias})
            examples.append(example)
        model.update(examples, losses=losses, drop=0.2)
    if epoca % 1 == 0:
        #historico.append(losses)
        print(f"Época {epoca}, perdas: {losses}")

model.to_disk('app/models/modelo_reacoes')
print('modelo treinado com sucesso')