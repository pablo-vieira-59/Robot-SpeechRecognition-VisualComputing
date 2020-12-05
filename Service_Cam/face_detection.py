import cv2 as cv
import numpy as np
from urllib.request import urlopen
import requests, os

# Camera URL
url = "http://10.0.0.29:8080/"

# Modelo de Reconhecimento Facial
net = cv.dnn.readNetFromCaffe('Models/deploy.prototxt.txt', 'Models/res10_300x300_ssd_iter_140000.caffemodel')
min_con = 0.9

def detect_faces(image, net, min_con):
	# Carregando Imagem e Transformando em Blob

	(h, w) = image.shape[:2]
	center_img_x = (w / 2)
	center_img_y = (h / 2)
	blob = cv.dnn.blobFromImage(cv.resize(image, (300, 300)), 1.0,
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
				#Turn Left
				requests.post('http://127.0.0.1:5002/send_command', json={"command":"a"})
			if center_detect_x < center_img_x - deadzone:
				#Turn Right
				requests.post('http://127.0.0.1:5002/send_command', json={"command":"d"})

			# Desenha a Caixa com a probabilidade
			text = "%.2f %%" % (confidence * 100)
			cv.rectangle(image, (startX, startY), (endX, endY),(0, 0, 255), 2)
			cv.putText(image, text, (startX, startY),cv.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
			cv.putText(image, 'Distance to Center : ' + str(dist), (startX, startY - 20),cv.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)

	# show the output image
	_ , frame = cv.imencode('.jpg',image)
	return frame

def get_stream(url):
    CAMERA_BUFFRER_SIZE=4096
    stream = urlopen(url)
    bts=b''
    i = 0
    img_hist = None

    while True:    
        try:
            bts += stream.read(CAMERA_BUFFRER_SIZE)
            jpghead = bts.find(b'\xff\xd8')
            jpgend = bts.find(b'\xff\xd9')
            if jpghead>-1 and jpgend>-1:
                jpg = bts[jpghead:jpgend+2]
                bts = bts[jpgend+2:]
                img = cv.imdecode(np.frombuffer(jpg,dtype=np.uint8),cv.IMREAD_UNCHANGED)

                if i < 0:
                    i += 1
                    yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + img_hist.tobytes() + b'\r\n\r\n')
                else:
                    img = detect_faces(img,net,min_con)
                    img_hist = img
                    i = 0
                    yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + img.tobytes() + b'\r\n\r\n')

        except Exception as e:
            print("Error:" + str(e))
            bts=b''
            stream=urlopen(url)
            continue