from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import GaussianNB

import pandas as pd
import numpy as np
import joblib

train = pd.read_csv('0-Intents.csv',sep=';')
x_train = train['speech']
y_train = train['intent']

vectorizer = CountVectorizer(ngram_range=(1,3))
x_train = vectorizer.fit_transform(x_train)
x_train = x_train.toarray()

model = GaussianNB()
model.fit(x_train,y_train)

score = model.score(x_train,y_train)
score = np.round(score*100,decimals=2)
print('Score : ', score)

joblib.dump(model,'model.joblib')
joblib.dump(vectorizer, 'vectorizer.joblib')