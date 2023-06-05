import threading
import time

Tc = 5
Ta_min = 1
Ta_max = 3


class Ponte:
    def __init__(self):
        self.max_carros_na_ponte = 5
        self.carros_na_ponte = 0
        self.mutex = threading.Semaphore(1)
        self.carros_cruzados_ida = 0
        self.carros_cruzados_volta = 0
        self.tempo_espera_total = 0
        self.tempo_utilizacao_ponte = 0
        self.tempo_total = 0

    def atravessar(self, carro):
        self.mutex.acquire()

        while self.carros_na_ponte >= self.max_carros_na_ponte:
            self.mutex.release()
            time.sleep(0.1)
            self.mutex.acquire()

        self.carros_na_ponte += 1
        self.mutex.release()

        if carro.sentido == "ida":
            print(
                f"Carro -> {threading.current_thread().name} atravessando a ponte no sentido {carro.sentido}")
            tempo_inicial = time.time()
            time.sleep(Tc)
            tempo_final = time.time()
            print(
                f"Carro -> {threading.current_thread().name} atravessou a ponte no sentido {carro.sentido}")
        else:
            print(
                f"Carro <- {threading.current_thread().name} atravessando a ponte no sentido {carro.sentido}")
            tempo_inicial = time.time()
            time.sleep(Tc)
            tempo_final = time.time()
            print(
                f"Carro <- {threading.current_thread().name} atravessou a ponte no sentido {carro.sentido}")

        self.mutex.acquire()
        self.carros_na_ponte -= 1
        if carro.sentido == "ida":
            self.carros_cruzados_ida += 1
        else:
            self.carros_cruzados_volta += 1
        self.tempo_espera_total += tempo_inicial - \
            (carro.identificador * Ta_max)
        self.tempo_utilizacao_ponte += tempo_final - tempo_inicial
        self.tempo_total += tempo_final - (carro.identificador * Ta_max)
        self.mutex.release()
