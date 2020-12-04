import os, joblib, json, requests
import pandas as pd
import numpy as np
import playsound as p
import numpy as np

from gtts import gTTS
from flask_cors import CORS
from flask import Flask, make_response, render_template, Request, jsonify

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

def speak(text, filename):
    tts = gTTS(text=text, lang='pt')
    tts.save(filename)
    p.playsound(filename)
        
def get_speech():
    request = requests.get("http://127.0.0.1:5004/chatbot_answer")
    r_json = request.text
    speech = json.loads(r_json)['speech']
    return speech

@app.route("/tts_status",methods=["GET","POST"])    
def get_status():
    return jsonify({'status':True})

@app.route("/tts_answer",methods=["GET","POST"])
def chat():
    ind = np.random.randint(0,9999999)
    filename = "output" + str(ind) + ".mp3"
    speech = get_speech()
    speak(speech, filename)
    os.remove(filename)
    return jsonify({'speech':speech})

if __name__ == "__main__":
    app.run(debug=True,port=5005,host="0.0.0.0")