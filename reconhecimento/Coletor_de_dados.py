import cv2
import os
import numpy

data_path = 'reconhecimento/dataset/User.'
face_classifier = cv2.CascadeClassifier('reconhecimento/haarcascade_frontalface_default.xml')

def capturar_rosto(frame):
    cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rostos = face_classifier.detectMultiScale(cinza, 1.3, 6)

    if rostos == ():
        return None

    for (x, y, w, h) in rostos:
        cropped_face = frame[y:y + h, x:x + w]

    return cropped_face

dic1 = []
def program(fotos):
    cap = cv2.VideoCapture(0)
    cont1 = 0
    while True:
        ret, frame = cap.read()
        imagem = frame

        if capturar_rosto(frame) is not None:
            cont1 += 1
            cv2.imshow('Rostos na sua webcam', imagem)

            face = cv2.resize(capturar_rosto(frame), (300, 300))
            face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

            # arquivo = data_path + str(id) + '.' + str(count) + '.jpg'
            dic1.append(face)
            # cv2.putText(face, str(count), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (168, 200, 173), 2)
            if cont1 >= fotos:
                return dic1

        else:
            cv2.imshow('Rostos na sua webcam', imagem)
            # print("Face Not Found")
            pass

        if cv2.waitKey(1) == ord('q'):
            return dic1

    cap.release()
    cv2.destroyAllWindows()
