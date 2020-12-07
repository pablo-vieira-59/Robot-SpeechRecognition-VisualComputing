from math import fabs
import requests
import speech_recognition as sr
import playsound as p
from flask_cors import CORS
from flask import Flask, jsonify

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
mic_status = False

@app.route("/speech_data",methods=["GET","POST"])
def listen_mic():
    global mic_status
    if not mic_status:
        mic_status = True
        phrase=""
        try:
            microfone = sr.Recognizer()
            with sr.Microphone() as source:
                microfone.adjust_for_ambient_noise(source)
                p.playsound('listen.mp3')
                print("Diga alguma coisa: ")
                audio = microfone.listen(source,timeout=2,phrase_time_limit=3)
                phrase = microfone.recognize_google(audio,language='pt-BR')
        except:
            pass
                
        p.playsound('end.mp3')

        ret = {"message":phrase}
        mic_status = False
        try:
            requests.post("http://127.0.0.1:5004/chatbot_answer", json=(ret))
            return jsonify(ret)
        except:
            print("Falha no serviço Chatbot")
            return jsonify({"message":"Falha no serviço Chatbot"})
    else:
        print("Serviço em Uso")
        return jsonify({"message":"Serviço em uso"})

@app.route("/speech_status",methods=["GET","POST"])
def get_status():
    return jsonify({'status':True})

if __name__ == "__main__":
    app.run(debug=True,port=5003,host="0.0.0.0")