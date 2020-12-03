import os, joblib, json, requests, pyttsx3, pythoncom, multiprocessing, time
import pandas as pd
import numpy as np

from flask_cors import CORS
from sklearn.feature_extraction.text import CountVectorizer
from flask import Flask, make_response, render_template, Request, jsonify
from sklearn.naive_bayes import GaussianNB


infos = pd.read_csv('1-Info.csv',sep=';')
infos = infos['speech']
skills = pd.read_csv('2-Skills.csv',sep=';')
skills = skills['speech']
jokes = pd.read_csv('3-Jokes.csv',sep=';')
jokes = jokes['speech']
greetings = pd.read_csv('4-Greetings.csv',sep=';')
greetings = greetings['speech']

data = [[],infos,skills,jokes,greetings]

vectorizer = joblib.load('vectorizer.joblib')
model = joblib.load('model.joblib')

tts = pyttsx3.init()
tts_voice = tts.getProperty('voices')
br_voice_id = tts_voice[0].id
for voice in tts_voice:
    print(voice.name)
    if voice.name == 'Microsoft Daniel - Portuguese (Brazil)':
        br_voice_id = voice.id
        break

tts.setProperty('voice',br_voice_id)

def speak(text):
    tts_voice = tts.getProperty('voices')
    tts.setProperty('voice',br_voice_id)
    tts.say(text)
    tts.runAndWait()
    return True

def start_speech(ans):
    p = multiprocessing.Process(target=speak, args=(ans,))
    p.start()

def get_prediction(speech):
    speech = vectorizer.transform([speech])
    speech = speech.toarray()
    prediction = model.predict(speech)
    prediction_prob = model.predict_proba(speech)
    prediction_prob = np.round(prediction_prob,3)
    print(prediction_prob)
    ind = prediction[0]
    ans = data[ind][np.random.randint(0,len(data[ind]))]
    start_speech(ans)
    return ans

def get_speech():
    try:
        request = requests.get("http://127.0.0.1:5003/speech_data")
        r_json = request.text
        speech = json.loads(r_json)['speech']
        return speech
    except:
        return ''
 
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/chatbot_status",methods=["GET","POST"])    
def get_status():
    return jsonify({'status':True})

@app.route("/chatbot_answer",methods=["GET","POST"])    
def chat():
    speech = get_speech()
    if speech == '':
        speech = 'Desculpe , não consegui ouvir'
        start_speech(speech)
    else:
        speech = get_prediction(speech)

    return jsonify({'message':speech})

if __name__ == "__main__":
    pythoncom.CoInitialize()
    app.run(debug=True,port=5004,host="0.0.0.0")