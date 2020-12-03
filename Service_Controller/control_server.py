from flask import Flask, make_response, render_template, Request, jsonify
from udp import UDPclient

import json
import numpy as np
import requests

udp_client = UDPclient("10.0.0.29",5900,1024)

app = Flask(__name__)

@app.route("/sensor_status",methods=["GET","POST"])    
def get_status():
    '''
    udp_client.send_message("r")
    msg = udp_client.receive_message(1)
    if(msg != None):
        return jsonify({'status':True})
    else:
        return jsonify({'status':False})
    '''
    return jsonify({'status':True})
       
if __name__ == "__main__":
    app.run(debug=True,port=5002,host="0.0.0.0")