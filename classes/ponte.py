import threading
import time


TA_MAX = 3
TC = 5


class Ponte:
    def __init__(self, P):
        self.max_carros_na_ponte = 5
        self.carros_na_ponte = 0
        self.mutex = threading.Lock()
        self.condition = threading.Condition(self.mutex)
        self.carros_cruzados_ida = 0
        self.carros_cruzados_volta = 0
        self.tempo_espera_total = 0
        self.tempo_utilizacao_ponte = 0
        self.tempo_total = 0
        self.P = P
        self.carros_atravessados = 0
        self.sentido_atual = "ida"

    def atravessar(self, carro):
        self.mutex.acquire()

        while self.carros_na_ponte >= self.max_carros_na_ponte or self.sentido_atual != carro.sentido:
            self.condition.wait()

        self.carros_na_ponte += 1
        self.carros_atravessados += 1
        self.condition.notifyAll()
        self.mutex.release()

        if carro.sentido == "ida":
            tempo_inicial = time.time()
            time.sleep(TC)
            tempo_final = time.time()
            print(
                f"Carro -> {carro.identificador} atravessou a ponte no sentido {carro.sentido}")
        else:
            tempo_inicial = time.time()
            time.sleep(TC)
            tempo_final = time.time()
            print(
                f"Carro <- {carro.identificador} atravessou a ponte no sentido {carro.sentido}")

        self.mutex.acquire()
        self.carros_na_ponte -= 1
        if carro.sentido == "ida":
            self.carros_cruzados_ida += 1
        else:
            self.carros_cruzados_volta += 1
        self.tempo_espera_total += tempo_inicial - (carro.identificador * TA_MAX)
        self.tempo_utilizacao_ponte += tempo_final - tempo_inicial
        self.tempo_total += tempo_final - (carro.identificador * TA_MAX)

        if self.carros_atravessados >= self.P:
            self.sentido_atual = "volta" if self.sentido_atual == "ida" else "ida"
            self.carros_atravessados = 0
        self.condition.notifyAll()
        self.mutex.release()
