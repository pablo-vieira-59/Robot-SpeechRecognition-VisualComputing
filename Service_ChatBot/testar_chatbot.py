import pandas, joblib, json, requests, unidecode, random
from datetime import datetime


answers = pandas.read_csv('Dados/Respostas.csv',sep=';')

model = joblib.load('Modelos/naive_bayes.joblib')
vectorizer = joblib.load('Modelos/vectorizer.joblib')

def make_prediction(text :str):
    text = vectorizer.transform([text])
    text = text.toarray()
    pred = model.predict(text)
    return pred[0]

def weather_response():
    request = requests.get("https://api.hgbrasil.com/weather?woeid=455839")
    request = request.text
    request = json.loads(request)['results']

    cidade = request['city_name']
    descricao = request['description']
    humidade = request['humidity']
    vento = request['wind_speedy']
    temperatura = request['temp']
    data = datetime.now().strftime("%d/%m/%H/%M").split('/')
    msg = "A previsão para %s é de %s , com temperatura de %s graus, humidade de %s porcento e vento de %s. Agora são %s e %s do dia %s do %s." % (cidade, descricao, temperatura, humidade, vento, data[2],data[3], data[0], data[1])
    return msg

def greeting_response(input_message :str):
    input_message = unidecode.unidecode(input_message)
    input_message = input_message.lower()
    greeting = 'Oi'
    common_greetings = ['ola','suave','boa noite','boa tarde','bom dia','salve','e ai']
    for greet in common_greetings:
        if greet in input_message:
            greeting = greet
            break
    possible_answers = get_answers_by_class('saudacao')
    answer = "%s%s%s" % (greeting, ', ' , possible_answers[random.randint(0, len(possible_answers)-1)])
    return answer

def common_responses(predicted_class :str):
    possible_answers = get_answers_by_class(predicted_class)
    answer = possible_answers[random.randint(0, len(possible_answers)-1)]
    return answer

def get_answers_by_class(predicted_class :str):
    possible_answers = list(answers.where(answers['intent']==predicted_class).dropna()['speech'])
    return possible_answers

def gen_response(predicted_class :str, input_message :str):
    response = 'Desculpe , não entendi.'
    if predicted_class == 'tempo':
        response = weather_response()
    elif predicted_class == 'saudacao':
        response = greeting_response(input_message)
    else:
        response = common_responses(predicted_class)
    return response

while 1:
    msg = input('Mensagem para o Chatbot:')
    pred = make_prediction(msg)
    print('Classe : %s' % (pred))
    print(gen_response(pred, msg))