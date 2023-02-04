import time
import cv2
from pymongo import MongoClient
import threading
import pyfirmata

pin = 13
port = 'COM7'
board = pyfirmata.Arduino(port)


client = MongoClient('URL')
db = client['Cluster0']
collection = db['trfse']

face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
model = cv2.face.LBPHFaceRecognizer_create()
model.read('recognizer/trainningData.yml')

fonte = cv2.FONT_HERSHEY_DUPLEX

def usuarios(id):
    user = collection.find_one({"_id": id})
    return str(user["nome"])

def face_detector(frame, size=0.5):
    cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rostos = face_classifier.detectMultiScale(cinza, 1.3, 5)
    if rostos == ():
        return frame, []

    for (x, y, w, h) in rostos:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
        roi = frame[y:y + h, x:x + w]
        roi = cv2.resize(roi, (300, 300))

        return frame, roi

def abrir():
    board.digital[5].write(1)
    time.sleep(15)
    board.digital[5].write(0)

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()

    imagem, face = face_detector(frame)

    try:
        face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
        result = model.predict(face)

        if result[1] < 500:
            ID = result[0]
            chance = int((1 - (result[1]) / 300) * 100)
            display_string = str(chance) + '% Chance de Ser Um Usuario'
            cv2.putText(imagem, display_string, (30, 50), fonte, 1, (0, 255, 255), 4)

            if chance > 80:
                user = usuarios(str(ID))
                cv2.putText(imagem, "Desbloquado", (200, 450), fonte, 1, (0, 255, 0), 4)
                cv2.putText(imagem, user, (200, 400), fonte, 1, (0, 255, 0), 4)
                cv2.imshow('Face Scanner', imagem)
                threading.Thread(target=abrir).start()

            else:
                cv2.putText(imagem, "Bloqueado", (200, 450), fonte, 1, (0, 0, 255), 4)
                cv2.imshow('Face Scanner', imagem)

    except:
        cv2.putText(imagem, "Rosto Sem Reconhecimento", (75, 450), fonte, 1, (0, 0, 255), 4)
        cv2.imshow('Face Scanner', imagem)
        pass

    if cv2.waitKey(1) == ord('q'):
        break
    time.sleep(0.1)


cap.release()
cv2.destroyAllWindows()

