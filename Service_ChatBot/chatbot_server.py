import os
import pandas as pd
import numpy as np
import playsound as p
import joblib
import json
import numpy as np
import requests

from gtts import gTTS
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
ind = 0

def speak(text, filename):
    tts = gTTS(text=text, lang='pt')
    tts.save(filename)
    p.playsound(filename)
    
def get_prediction(speech, filename):
    speech = vectorizer.transform([speech])
    speech = speech.toarray()
    prediction = model.predict(speech)
    ind = prediction[0]
    ans = data[ind][np.random.randint(0,len(data[ind]))]
    speak(ans, filename)
    return ans
    
def get_speech():
    request = requests.get("http://127.0.0.1:5003/speech_data")
    r_json = request.text
    speech = json.loads(r_json)['speech']
    return speech
 
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/chatbot_status",methods=["GET","POST"])    
def get_status():
    return jsonify({'status':True})

@app.route("/chatbot_answer",methods=["GET","POST"])    
def chat():
    ind = np.random.randint(0,9999999)
    filename = "output" + str(ind) + ".mp3"
    try:
        speech = get_speech()
        speech = get_prediction(speech, filename)
    except:
        speech = 'Desculpe , não consegui ouvir.'
        speak(speech, filename)
    os.remove(filename)
    return jsonify({'message':speech})

if __name__ == "__main__":
    app.run(debug=True,port=5004,host="0.0.0.0")



