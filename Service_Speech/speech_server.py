import json

import speech_recognition as sr
import playsound as p

from flask_cors import CORS
from flask import Flask, jsonify

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/speech_data",methods=["GET","POST"])
def ouvir_microfone():
    frase=""
    microfone = sr.Recognizer()
    with sr.Microphone() as source:
        microfone.adjust_for_ambient_noise(source)
        p.playsound('listen.mp3')
        print("Diga alguma coisa: ")
        audio = microfone.listen(source,timeout=2,phrase_time_limit=3)
        try:
            frase = microfone.recognize_google(audio,language='pt-BR')
        except sr.UnkownValueError:
            print("Não entendi")
            
    p.playsound('end.mp3')
    return jsonify({'speech':frase})

@app.route("/speech_status",methods=["GET","POST"])
def get_status():
    return jsonify({'status':True})

if __name__ == "__main__":
    app.run(debug=True,port=5003,host="0.0.0.0")