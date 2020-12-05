from flask import Flask, Response, jsonify
import face_detection, objects_detection
import numpy as np
import urllib.request as ur
import cv2

camera_url = "http://10.0.0.29"


app = Flask(__name__)

@app.route("/video_feed",methods=["GET","POST"])
def video_feed():
	resp = Response(face_detection.get_stream(camera_url + ":8081/"), mimetype='multipart/x-mixed-replace; boundary=frame')
	return resp

@app.route("/detect_objects",methods=["GET","POST"])
def detect_objects():
	img = ur.request.urlopen(camera_url + "8080/capture")
	img = np.array(bytearray(img.read()),dtype=np.uint8)
	img = cv2.imdecode(img,-1)

	detection_message = objects_detection.yolo_description(img)

	return jsonify({"message":detection_message})

@app.route("/cam_status", methods=["GET","POST"])
def get_status():
	try:
		ur.urlopen(face_detection.url,timeout=1)
		return jsonify({'status':True})
	except:
		return jsonify({'status':False})

if __name__ == "__main__":
	app.run(debug=True,port=5001,host="0.0.0.0")
