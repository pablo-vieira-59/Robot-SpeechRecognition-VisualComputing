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
    global search_status
    msg = ""
    if not search_status:
        search_status = True
        msg = "O Que você quer que eu procure?"
    else:
        if 'Cancel' in input_message:
            msg = 'Pesquisa Cancelada'
        else:
            wikipedia.set_lang("pt")
            try:
                msg_wait = {"message":"Estou pesquisando , aguarde um momento."}
                try:
                    requests.post("http://127.0.0.1:5005/tts_speak", json=msg_wait)
                except:
                    print("Falha no serviço TTS")
                    
                search = wikipedia.search(input_message)
                search = wikipedia.page(search[0]).content
                search = search.split('.')[0]

                result = re.sub("[\(\[].*?[\)\]]", "", search)
                search_status = False
                msg = "Consegui encontrar isso: %s " % (result)
            except:
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
    
def subclass_response(predicted_class :str,input_message :str):
    predicted_subclass,_ = make_prediction(input_message, model_information)
    possible_answers = get_answers_by_subclass(predicted_class, predicted_subclass)
    index = random.randint(0, len(possible_answers)-1)
    answer = possible_answers[index]
    return answer

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
    response = 'Desculpe , não entendi.'

    if input_message == "":
        return response

    if search_status:
        response = search_response(input_message)
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

    else:
        response = common_responses(predicted_class)

    return response

def set_false(var):
    var = False
    return var

answers = pandas.read_csv('Dados/Respostas.csv',sep=';')

model_common = joblib.load('Modelos/classificador_geral.joblib')
model_information = joblib.load('Modelos/classificador_informacao.joblib')
model_weather = joblib.load('Modelos/classificador_tempo.joblib')
vectorizer = joblib.load('Modelos/vectorizer.joblib')

search_status = False
