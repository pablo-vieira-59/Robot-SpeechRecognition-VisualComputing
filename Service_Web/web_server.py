from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def main():
    return render_template("index.html")

@app.route("/components",methods=["GET","POST"])
def components():
    return render_template("components.html")

@app.route("/documentation",methods=["GET","POST"])
def documentation():
    return render_template("documentation.html")

@app.route("/images",methods=["GET","POST"])
def images():
    return render_template("images.html")

@app.route("/data",methods=["GET","POST"])
def services_status():
    cam_status = get_status("http://127.0.0.1:5001/cam_status")
    #sensor_status = get_status("http://127.0.0.1:5002/sensor_status")
    sensor_status = True
    speech_status = get_status("http://127.0.0.1:5003/speech_status")
    chatbot_status = get_status("http://127.0.0.1:5004/chatbot_status")
    tts_status = get_status("http://127.0.0.1:5005/tts_status")
    ans = {'cam_status':cam_status,'sensor_status':sensor_status,'speech_status':speech_status,'chatbot_status':chatbot_status,'tts_status':tts_status}
    return jsonify(ans)
    
def get_status(uri :str):
    try:
        response = requests.get(uri, timeout=0.5)
        response = response.json()
        status = response['status']
        return status
    except:
        return False

if __name__ == "__main__":
    app.run(debug=True,port=80,host="0.0.0.0")