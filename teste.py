"""import reconhecimento.Coletor_de_dados as cd
import cv2


data_path = 'reconhecimento/dataset/User.'
id = 0
f1 = cd.program(id, 10)
print(f1)
count = 0
for face in f1:
    cv2.imwrite(data_path + str(id) + '.' + str(count) + '.jpg', face)
    cv2.putText(face, str(count), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (168, 200, 173), 2)
    count += 1"""
import time

import pyfirmata  # Importamos a biblioteca PyFirmata que realiza a comunicação entre Python e Arduino
from time import sleep # Importamos também a biblioteca padrão Time, com o objetivo de setar as pausas e marcações temporais entre as piscadas.
import threading


pin = 13  # Definimos para o Python que nosso pino é o 13.
port = 'COM7'  # Configuramos a porta como a porta COM4. Esta configuração deve ser alterada caso sua placa não se configure nesta porta.
board = pyfirmata.Arduino(port)  # Criamos a variável board que realizará os comandos a partir daqui

def tarefa1():
    while 10:
        board.digital[5].write(1)  # Utilizamos a variável board e seu método .Digital para dizer ao pino 13 que ele deve acender
        sleep(5)  # Colocamos uma pausa de 0.01 segundos
        board.digital[5].write(0)  # Utilizamos a variável board e seu método .Digital para dizer ao pino 13 que ele deve apagar
        sleep(5)

def tarefa2():
    while 10:
        print("ON")
        time.sleep(5)
        print("OFF")
        time.sleep(5)

threading.Thread(target=tarefa1).start()
tarefa2()




