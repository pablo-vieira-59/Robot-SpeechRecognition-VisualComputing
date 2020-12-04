from flask import Flask, make_response, render_template, Request, jsonify
import json
import numpy as np
import requests

app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def main():
    return render_template("index.html")

@app.route("/components",methods=["GET","POST"])
def components():
    return render_template("components.html")

@app.route("/data",methods=["GET","POST"])
def services_status():
    cam_status = get_status("http://127.0.0.1:5001/cam_status")
    sensor_status = get_status("http://127.0.0.1:5002/sensor_status")
    speech_status = get_status("http://127.0.0.1:5003/speech_status")
    chatbot_status = get_status("http://127.0.0.1:5004/chatbot_status")
    tts_status = get_status("http://127.0.0.1:5005/tts_status")
    return jsonify({'cam_status':cam_status,'sensor_status':sensor_status,'speech_status':speech_status,'chatbot_status':chatbot_status,'tts_status':tts_status})
    
def get_status(uri :str):
    try:
        response = requests.get(uri)
        response = response.text
        response = json.loads(response)
        status = response['status']
        return status
    except:
        return False

if __name__ == "__main__":
    app.run(debug=True,port=80,host="0.0.0.0")