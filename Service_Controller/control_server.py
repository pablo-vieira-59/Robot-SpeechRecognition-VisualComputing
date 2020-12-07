from flask import Flask, jsonify, request
from flask_cors import CORS
from udp import UDPclient
import requests, time, multiprocessing

udp_client = UDPclient("10.0.0.29",5900,1024)
sensor_status = False

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/send_command",methods=["GET","POST"])    
def send_command():
    content = request.json
    udp_client.send_message(content['command'])
    return jsonify({'answer':content['command']})

@app.route("/get_info", methods=["GET", "POST"])
def get_info():
    content = request.json
    udp_client.send_message(content['command'])
    ans = udp_client.receive_message(timeout=1)
    if ans is not None:
        return jsonify({'answer': ans})
    else:
        return jsonify({'answer': 'None'})

@app.route("/sensor_status",methods=["GET","POST"])    
def get_status():
    return jsonify({'status':True})

def check_sensor():
    while True:
        udp_client.send_message('r')
        ans = udp_client.receive_message(timeout=1)
        print(ans)
        if ans is not None:
            ans = float(ans)
            if ans < 10:
                try:
                    requests.get("http://127.0.0.1:5003/speech_data")
                except:
                    print('Falha no serviço Speech')
        time.sleep(.5)

if __name__ == "__main__":
    p = multiprocessing.Process(target=check_sensor)
    p.start()
    app.run(debug=True,port=5002,host="0.0.0.0")
