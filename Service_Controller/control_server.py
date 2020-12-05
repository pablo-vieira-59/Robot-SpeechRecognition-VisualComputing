from flask import Flask, jsonify, request
from flask_cors import CORS
from udp import UDPclient

udp_client = UDPclient("10.0.0.29",5900,1024)

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/send_command",methods=["GET","POST"])    
def send_command():
    content = request.json
    udp_client.send_message(content['command'])
    return jsonify({'command':content['command']})

@app.route("/sensor_status",methods=["GET","POST"])    
def get_status():
    return jsonify({'status':True})
       
if __name__ == "__main__":
    app.run(debug=True,port=5002,host="0.0.0.0")