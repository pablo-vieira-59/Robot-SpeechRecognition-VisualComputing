from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import cross_val_score

import pandas as pd
import numpy as np
import joblib, glob


def load_datasets():
    dataset = pd.DataFrame()
    paths = glob.glob('Dados/*.txt')
    for path in paths:
        intent = path.split('\\')[1].split('.')[0]
        data = pd.read_csv(path,names=['speech'])
        data['intent'] = intent
        dataset = dataset.append(data)
    return dataset

def train_subtype(datset_path :str, vectorizer :CountVectorizer):
    intent = datset_path.split('\\')[1].split('.')[0]
    data = pd.read_csv(datset_path, names=['speech','subclass'],sep=';')

    x_train = data['speech']
    y_train = data['subclass']

    x_train = vectorizer.transform(x_train)
    x_train = x_train.toarray()

    model = GaussianNB(var_smoothing=0.00001)
    score = cross_val_score(model, x_train, y_train)
    print('Score %s: %.2f' % (intent,np.mean(score)))

    model.fit(x_train, y_train)

    joblib.dump(model,'Modelos/classificador_%s.joblib' % (intent))

def train_base_model(data :pd.DataFrame, vectorizer :CountVectorizer):
    x_train = data['speech']
    y_train = data['intent']

    x_train = vectorizer.transform(x_train)
    x_train = x_train.toarray()

    model = GaussianNB(var_smoothing=0.01)
    score = cross_val_score(model, x_train, y_train)
    print('Score : %.2f' % (np.mean(score)))

    model.fit(x_train, y_train)

    joblib.dump(model,'Modelos/classificador_geral.joblib')

dataset = load_datasets()
count_vectorizer = CountVectorizer(ngram_range=(1,3), strip_accents='ascii', lowercase=True, analyzer='char')
count_vectorizer.fit_transform(dataset['speech'])
joblib.dump(count_vectorizer, 'Modelos/vectorizer.joblib')

train_base_model(dataset, count_vectorizer)
train_subtype('Dados\\informacao.txt', count_vectorizer)
train_subtype('Dados\\tempo.txt', count_vectorizer)
train_subtype('Dados\\sentimento.txt', count_vectorizer)
