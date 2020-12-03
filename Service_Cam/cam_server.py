from flask import Flask, make_response, render_template, Response, jsonify
import json
import numpy as np
import cv2
import urllib.request as ur

ip = "10.0.0.29"
url = "http://"+ip+"/capture"
net = cv2.dnn.readNetFromCaffe('deploy.prototxt.txt', 'res10_300x300_ssd_iter_140000.caffemodel')
min_con = 0.9

app = Flask(__name__)

def detect_faces(url, net, min_con):
	# Carregando Imagem e Transformando em Blob
	image = ur.urlopen(url,timeout=2)
	image = np.array(bytearray(image.read()),dtype=np.uint8)
	image = cv2.imdecode(image,-1)
	(h, w) = image.shape[:2]
	center_img_x = (w / 2)
	center_img_y = (h / 2)
	blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0,
		(300, 300), (104.0, 177.0, 123.0))

	# Passando Blob para Modelo e Recebendo Detecções
	net.setInput(blob)
	detections = net.forward()
	
	# Loop pelas detecções
	for i in range(0, detections.shape[2]):
		# Extrai a Confiança
		confidence = detections[0, 0, i, 2]

		# Filtragem de Confiança
		if confidence > min_con:
			# Pega cordena X e Y da detecção
			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")
			center_detect_x = (startX + endX) / 2
			center_detect_y = (startY + endY) / 2
	
			# Controlando Robo
			deadzone = 20
			dist = center_img_x - center_detect_x
			if center_detect_x > center_img_x + deadzone:
				print('Turn Left')
				print('Distance to Center: ' + str(dist))
			if center_detect_x < center_img_x - deadzone:
				print('Turn Right')
				print('Distance to Center: ' + str(dist))

			# Desenha a Caixa com a probabilidade
			text = "{:.2f}%".format(confidence * 100)
			y = startY - 10 if startY - 10 > 10 else startY + 10
			cv2.rectangle(image, (startX, startY), (endX, endY),
				(0, 0, 255), 2)
			cv2.putText(image, text, (startX, y),
				cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
			cv2.putText(image, 'Distance to Center : ' + str(dist), (startX, y - 20),
				cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)

	# show the output image
	retval , frame = cv2.imencode('.png',image)
	return frame


def process_image():
    while True:
        img = detect_faces(url,net,min_con)
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + img.tobytes() + b'\r\n\r\n')


@app.route("/video_feed",methods=["GET","POST"])
def video_feed():
    return Response(process_image(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/cam_status", methods=["GET","POST"])
def get_status():
	'''
    try:
        image = ur.urlopen(url,timeout=.2)
        return jsonify({'status':True})
    except:
        return jsonify({'status':False})
	'''
	return jsonify({'status':True})
    

if __name__ == "__main__":
    app.run(debug=True,port=5001,host="0.0.0.0")
	