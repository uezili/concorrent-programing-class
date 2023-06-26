import threading
import random
import time

Ta_min = 1
Ta_max = 3

class Caminhao(threading.Thread):
    def __init__(self, identificador, sentido, ponte):
        super().__init__()
        self.identificador = identificador
        self.sentido = sentido
        self.ponte = ponte

    def run(self):
        tempo_chegada = random.uniform(Ta_min, Ta_max)
        time.sleep(tempo_chegada)
        self.ponte.atravessar(self)
