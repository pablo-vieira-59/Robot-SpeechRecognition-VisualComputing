import json, requests, pyttsx3, pythoncom, multiprocessing
from flask_cors import CORS
from flask import Flask, request, jsonify

tts = pyttsx3.init()
tts_voice = tts.getProperty('voices')
br_voice_id = tts_voice[0].id
for voice in tts_voice:
    print(voice.name)
    if voice.name == 'Microsoft Daniel - Portuguese (Brazil)':
        br_voice_id = voice.id
        break

tts.setProperty('voice',br_voice_id)

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

def speak(text):
    global tts
    #tts_voice = tts.getProperty('voices')
    #tts.setProperty('voice',br_voice_id)
    tts.say(text)
    tts.runAndWait()
    return True

def start_speech(ans):
    p = multiprocessing.Process(target=speak, args=(ans,))
    p.start()

@app.route("/tts_status",methods=["GET","POST"])    
def get_status():
    return jsonify({'status':True})

@app.route("/tts_speak",methods=["GET","POST"])    
def chat():
    content = request.json
    speech = content['message']
    start_speech(speech)
    return jsonify({'speech':speech})

if __name__ == "__main__":
    pythoncom.CoInitialize()
    app.run(debug=True,port=5005,host="0.0.0.0")