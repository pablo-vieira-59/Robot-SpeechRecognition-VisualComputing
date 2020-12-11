from pickle import FALSE
import pandas, joblib, json, requests, unidecode, random
import numpy as np
import requests
from datetime import datetime

import wikipedia
import re

def make_prediction(text :str, model):
    text = vectorizer.transform([text])
    text = text.toarray()
    pred = model.predict(text)
    prob = model.predict_proba(text)
    return pred[0], np.max(prob[0]) * 100

def weather_response(input_message :str):
    pred,_ = make_prediction(input_message, model_weather)
    msg = ""
    if int(pred) == 1:
        try:
            request = requests.get("https://api.hgbrasil.com/weather?woeid=455839")
            request = request.text
            request = json.loads(request)['results']

            cidade = request['city_name']
            descricao = request['description']
            humidade = request['humidity']
            vento = request['wind_speedy']
            temperatura = request['temp']

            msg = "A previsão para %s é de %s , com temperatura de %s graus, humidade de %s porcento e vento de %s" % (cidade, descricao, temperatura, humidade, vento)

        except:
            msg = "Desculpe, Serviço indisponível no momento."

    elif int(pred) == 2:
        data = datetime.now().strftime("%d/%m/%H/%M").split('/')
        msg = "Agora são %s e %s do dia %s do %s." % (data[2],data[3], data[0], data[1])

    return msg

def greeting_response(input_message :str):
    input_message = unidecode.unidecode(input_message)
    input_message = input_message.lower()
    greeting = 'Oi'
    common_greetings = ['ola','suave','boa noite','boa tarde','bom dia','salve','e ai', 'tudo bom', 'tudo bem']
    for greet in common_greetings:
        if greet in input_message:
            greeting = greet
            break
    possible_answers = get_answers_by_class('saudacao')
    answer = "%s%s%s" % (greeting, ', ' , possible_answers[random.randint(0, len(possible_answers)-1)])
    return answer

def search_response(input_message :str):
    global SEARCH_STATUS
    msg = ""
    if not SEARCH_STATUS:
        SEARCH_STATUS = True
        msg = "O Que você quer que eu procure?"
    else:
        if 'Cancel' in input_message:
            msg = 'Pesquisa Cancelada'
        else:
            wikipedia.set_lang("pt")
            try:
                print("Estou pesquisando , aguarde um momento.")
                msg_wait = {"message":"Estou pesquisando , aguarde um momento."}
                try:
                    requests.post("http://127.0.0.1:5005/tts_speak", json=msg_wait)
                except:
                    print("Falha no serviço TTS")
                    
                search = wikipedia.search(input_message)
                search = wikipedia.page(search[0]).content
                search = search.split('.')[0]

                result = re.sub("[\(\[].*?[\)\]]", "", search)
                SEARCH_STATUS = False
                msg = "Consegui encontrar isso: %s " % (result)
            except:
                SEARCH_STATUS = False
                msg = "Desculpe , Não consegui encontrar nada"
    return msg

def objects_detection_response():
    try:
        req = requests.get("http://127.0.0.1:5001/detect_objects")
        r_json = req.text
        speech = json.loads(r_json)['message']
        return speech
    except:
        return "Desculpe, Serviço indisponivel no momento."

def common_responses(predicted_class :str):
    possible_answers = get_answers_by_class(predicted_class)
    index = random.randint(0, len(possible_answers)-1)
    answer = possible_answers[index]
    return answer

def tasks_responses(input_message :str):
    global TASK_STATUS
    global TASK_ID
    global TASKS
    global TASKS_PATH

    if not TASK_STATUS:
        pred,_ = make_prediction(input_message, model_task)
        pred = int(pred)
        msg = ""
        
        if pred == 1:
            TASK_STATUS = True
            TASK_ID = 1
            return "O que você quer que eu adicione?"
        elif pred == 2:
            TASK_STATUS = True
            TASK_ID = 2
            return "O que você quer que eu remova?"
        elif pred == 3:
            msg = ",".join(TASKS)
            msg = "Você tem as seguintes tarefas: " + msg
            return msg
    else:
        if not ('Cancel' in input_message):
            if TASK_ID == 1:
                TASKS.append(input_message)
                dataframe = pandas.DataFrame(TASKS, columns=["Tarefas"])
                dataframe.to_csv(TASKS_PATH, sep=";",columns=["Tarefas"],index=False)
                TASK_STATUS = False
                return "%s %s %s" % ("Tarefa :", input_message, ",Foi adicionada.")
            elif TASK_ID == 2:
                try:
                    TASKS.remove(input_message)
                    dataframe = pandas.DataFrame(TASKS, columns=["Tarefas"])
                    dataframe.to_csv(TASKS_PATH, sep=";",columns=["Tarefas"],index=False)
                    TASK_STATUS = False
                    return "%s %s %s" % ("Tarefa :", input_message, ",Foi removida.")
                except Exception as e:
                    print(e)
                    return "Desculpe , não encontrei essa tarefa para remover. Tente falar de novo , ou use o comando Cancelar para sair."
        else:
            TASK_STATUS = False
            return 'Tarefas Cancelado'
    
def subclass_response(predicted_class :str,input_message :str):
    predicted_subclass,_ = make_prediction(input_message, model_information)
    possible_answers = get_answers_by_subclass(predicted_class, predicted_subclass)
    index = random.randint(0, len(possible_answers)-1)
    answer = possible_answers[index]
    return answer

def jokes_responses():
    global JOKES
    ind = np.random.randint(0, len(JOKES)-1)
    joke = JOKES['charada'][ind]
    return joke

def get_answers_by_class(predicted_class :str):
    filter_1 = answers['intent']==predicted_class
    possible_answers = list(answers.where(filter_1).dropna()['speech'])
    return possible_answers

def get_answers_by_subclass(predicted_class :str, predicted_subclass :int):
    filter_1 = answers['intent'] == predicted_class
    filter_2 = answers['subclass'].astype(int) == predicted_subclass
    possible_answers = answers.where(filter_1).dropna()
    possible_answers = list(possible_answers.where(filter_2).dropna()['speech'])
    return possible_answers

def gen_response(predicted_class :str, input_message :str):
    global SEARCH_STATUS
    global TASK_STATUS
    
    response = 'Desculpe , não entendi.'
    
    if input_message == "":
        return response

    if SEARCH_STATUS:
        response = search_response(input_message)
        return response

    if TASK_STATUS:
        response = tasks_responses(input_message)
        return response

    if predicted_class == 'tempo':
        response = weather_response(input_message)
    elif predicted_class == 'saudacao':
        response = greeting_response(input_message)
    elif predicted_class == 'informacao':
        response = subclass_response('informacao',input_message)
    elif predicted_class == 'sentimento':
        response = subclass_response('sentimento',input_message)
    elif predicted_class == 'pesquisa':
        response = search_response(input_message)
    elif predicted_class == 'deteccao':
        response = objects_detection_response()
    elif predicted_class == 'tarefas':
        response = tasks_responses(input_message)
    elif predicted_class == 'piada':
        response = jokes_responses()

    else:
        response = common_responses(predicted_class)

    return response

answers = pandas.read_csv("Dados/Respostas.csv",sep=';')

JOKES = pandas.read_csv("Persistente/Lista de Piadas.csv",sep=';')

TASKS_PATH = "Persistente/Lista de Tarefas.txt"
TASKS = pandas.read_csv(TASKS_PATH,sep=";",names=['Tarefas'])
TASKS = list(TASKS["Tarefas"])
TASKS = TASKS[1:len(TASKS)]

model_common = joblib.load("Modelos/classificador_geral.joblib")
model_information = joblib.load("Modelos/classificador_informacao.joblib")
model_weather = joblib.load("Modelos/classificador_tempo.joblib")
model_task = joblib.load("Modelos/classificador_tarefas.joblib")
vectorizer = joblib.load("Modelos/vectorizer.joblib")

SEARCH_STATUS = False
TASK_STATUS = False
TASK_ID = 0
