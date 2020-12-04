from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import cross_val_score

import pandas as pd
import numpy as np
import joblib

train = pd.read_csv('Dados/Intents.csv',sep=';')
print(train)

x_train = train['speech']
y_train = train['intent']

vectorizer = CountVectorizer(ngram_range=(1,3),strip_accents='ascii')
x_train = vectorizer.fit_transform(x_train)
x_train = x_train.toarray()

model = GaussianNB()
score = cross_val_score(model, x_train, y_train)
print('Score : %.2f' % (np.mean(score)))

model.fit(x_train, y_train)

joblib.dump(model,'Modelos/naive_bayes.joblib')
joblib.dump(vectorizer, 'Modelos/vectorizer.joblib')