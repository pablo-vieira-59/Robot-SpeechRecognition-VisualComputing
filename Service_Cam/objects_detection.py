import cv2 as cv
import numpy as np

LABELS = open("Models/coco.names").read().strip().split("\n")
np.random.seed(59)
COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),	dtype="uint8")
YOLO_NET = cv.dnn.readNetFromDarknet("Models/yolov3.cfg", "Models/yolov3.weights")
LAYER_NAMES = YOLO_NET.getLayerNames()
LAYER_NAMES = [LAYER_NAMES[i[0] - 1] for i in YOLO_NET.getUnconnectedOutLayers()]
CONFIDENCE = 0.3

def detect_objetcs(frame):
    # Contruindo Blob e Passando Para Rede
    blob = cv.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    YOLO_NET.setInput(blob)
    layerOutputs = YOLO_NET.forward(LAYER_NAMES)
    return layerOutputs

def get_detection_info(layerOutputs, frame):
    # Pegando informacao da imagem
    (H,W) = frame.shape[:2]

    # Inicializando Arrays
    boxes = []
    confidences = []
    classIDs = []

    for output in layerOutputs:
        for detection in output:
            # Pega a classe e Confiança
            scores = detection[5:]
            classID = np.argmax(scores)
            conf = scores[classID]

            # Filtra as detecções mais fracas
            if conf > CONFIDENCE:
                # Cria o tamanho da Caixa
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")

                # Usa o X e Y das Caixas para achar as Arestas
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))

                # Atualiza as Listas
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(conf))
                classIDs.append(classID)

    # Aplica Supressão Non-Maxima , para eliminar detecções fracas e caixas entrelaçadas
    idxs = cv.dnn.NMSBoxes(boxes, confidences, CONFIDENCE, CONFIDENCE)
    idxs = idxs.flatten()

    return idxs, boxes, confidences, classIDs

def get_description(idxs, classIDs):
    detected_objetcs = []
    count_objects = []
    for i in idxs:
        object_name = LABELS[classIDs[i]]
        if object_name in detected_objetcs:
            idx = detected_objetcs.index(object_name)
            count_objects[idx] += 1
        else:
            detected_objetcs.append(object_name)
            count_objects.append(1)

    message = "Eu consegui identificar "
    for i in range(0, len(detected_objetcs)):
        if i == (len(detected_objetcs)-1):
            message += "e %i %s." % (count_objects[i], detected_objetcs[i])
        else:
            message += ", %i %s " % (count_objects[i], detected_objetcs[i])

    return message

def draw_detection_boxes(idxs, boxes, classIDs, confidences):
    # Garante que pelo Menos 1 detecção foi feita
    if len(idxs) > 0:
        # Passa Pelos indices das detecções
        for i in idxs:
            # Extrai a caixa
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])

            # Desenha a Caixa
            color = [int(c) for c in COLORS[classIDs[i]]]
            cv.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            text = "%s: %.2f" % (LABELS[classIDs[i]], confidences[i])
            cv.putText(frame, text, (x, y - 5), cv.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    return frame

def yolo_detection(image):
    output = detect_objetcs(image)
    idxs, boxes, confidences, classIDs = get_detection_info(output, image)
    frame = draw_detection_boxes(idxs, boxes, classIDs, confidences)
    return frame

def yolo_description(image):
    output = detect_objetcs(image)
    idxs, _, _, classIDs = get_detection_info(output, image)
    msg = "Desculpe, não consegui identificar nada."
    if len(idxs) > 0:
        msg = get_description(idxs, classIDs)
        
    return msg

