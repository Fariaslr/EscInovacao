# 1. Importando bibliotecas
import pandas as pd
import string
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
from nltk.corpus import stopwords
import nltk
import kagglehub
from kagglehub import KaggleDatasetAdapter

nltk.download('stopwords')

file_path = "spam.csv"
df = pd.read_csv('spam.csv', encoding='latin-1')[['v1', 'v2']]

df = df[['v1', 'v2']]
df.columns = ['label', 'message']

# 3. Pré-processamento
def preprocess(text):
    text = text.lower()  # minúsculas
    text = re.sub(r'\d+', '', text)  # remove números
    text = text.translate(str.maketrans('', '', string.punctuation))  # remove pontuação
    tokens = text.split()  # tokenização
    tokens = [word for word in tokens if word not in stopwords.words('english')]  # remove stopwords
    return ' '.join(tokens)

df['message'] = df['message'].apply(preprocess)

# 4. Vetorização e divisão treino/teste
X = df['message']
y = df['label']

vectorizer = CountVectorizer()
X_vectorized = vectorizer.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_vectorized, y, test_size=0.2, random_state=42)

# 5. Treinamento com Naive Bayes
model = MultinomialNB()
model.fit(X_train, y_train)

# 6. Avaliação
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# 7. Função para classificar novas mensagens
def classificar_nova_mensagem(mensagem):
    mensagem_processada = preprocess(mensagem)
    mensagem_vectorizada = vectorizer.transform([mensagem_processada])
    resultado = model.predict(mensagem_vectorizada)
    return resultado[0]

# Exemplo de uso:
nova_mensagem = "Congratulations! You won a free ticket to Bahamas. Text now!"
print("Classificação:", classificar_nova_mensagem(nova_mensagem))

