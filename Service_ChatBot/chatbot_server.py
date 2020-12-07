import requests
from flask_cors import CORS
from flask import Flask, request, jsonify
import chatbot
 
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/chatbot_status",methods=["GET","POST"])    
def get_status():
    return jsonify({'status':True})

@app.route("/chatbot_answer",methods=["GET","POST"])    
def chat():
    content = request.json
    speech = content["message"]
    pred, _ = chatbot.make_prediction(speech, chatbot.model_common)
    phrase = chatbot.gen_response(pred, speech)

    ret = {"message":phrase}
    try:
        requests.post("http://127.0.0.1:5005/tts_speak", json=(ret))
        return jsonify(ret)
    except:
        print("Falha no serviço TTS")
        return jsonify({"message":"Falha no serviço TTS"})

if __name__ == "__main__":
    app.run(debug=True,port=5004,host="0.0.0.0")