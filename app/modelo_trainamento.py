import string
import pandas as pd
import spacy
import re
import random
from spacy.lang.en.stop_words import STOP_WORDS

dataset=pd.read_csv("C:/Users/rapha/VSCodeProjects/tcc_machine_learning/app/models/data.csv", encoding='utf-8')

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
    Tweets = re.sub(r'[\U00010000-\U0010ffff]]', '', Tweets)
    
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

#criar modelo em branco para ingles
model = spacy.blank('pt')

categorias = model.add_pipe('textcat')

categorias.add_label('HAPPY')
categorias.add_label('SAD')
categorias.add_label('FEAR')
categorias.add_label('DISGUST')

historico = []

from spacy.training.example import Example

model.initialize()

for epoca in range(1000):
    random.shuffle(dataset_final)
    losses = {}
    for batch in spacy.util.minibatch(dataset_final, 30):
        examples = []
        for Tweets, categorias in batch:
            doc = model.make_doc(Tweets)
            example = Example.from_dict(doc, {"cats": categorias})
            examples.append(example)
        model.update(examples, losses=losses)
    if epoca % 100 == 0:
        historico.append(losses)

model.to_disk('modelo_reacoes')
print('modelo treinado com sucesso')