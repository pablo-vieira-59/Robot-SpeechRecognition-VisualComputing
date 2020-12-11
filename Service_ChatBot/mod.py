from os import sep
import pandas as pd

data = pd.read_csv("Persistente/Lista de Piadas.csv")
data = data.drop(['id','createdAt','updatedAt'],axis=1)
data['charada'] = data['pergunta'] + ' ' +data['resposta']
data = data.drop(['pergunta','resposta'],axis=1)
data.to_csv("Persistente/Lista de Piadas B.csv",sep=";")