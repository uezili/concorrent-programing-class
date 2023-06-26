import threading
import random
import time

class Carro(threading.Thread):
    def __init__(self, identificador, sentido, ponte):
        super().__init__()
        self.identificador = identificador
        self.sentido = sentido
        self.ponte = ponte

    def run(self):
        tempo_chegada = random.uniform(Ta_min, Ta_max)
        time.sleep(tempo_chegada)
        self.ponte.atravessar(self)

class Caminhao(threading.Thread):
    def __init__(self, identificador, sentido, ponte):
        super().__init__()
        self.identificador = identificador
        self.sentido = sentido
        self.ponte = ponte

    def run(self):
        tempo_chegada = random.uniform(Ta_min, Ta_max)
        time.sleep(tempo_chegada)
        self.ponte.atravessar_caminhao(self)

class Ponte:
    def __init__(self, P, U):
        self.max_carros_na_ponte = 5
        self.max_caminhoes_na_ponte = 1
        self.carros_na_ponte = 0
        self.caminhoes_na_ponte = 0
        self.mutex = threading.Lock()
        self.condicao = threading.Condition(self.mutex)
        self.carros_cruzados_ida = 0
        self.carros_cruzados_volta = 0
        self.caminhoes_cruzados_ida = 0
        self.caminhoes_cruzados_volta = 0
        self.tempo_espera_total = 0
        self.tempo_utilizacao_ponte = 0
        self.tempo_total = 0
        self.P = P
        self.U = U
        self.carros_atravessados_ida = 0
        self.carros_atravessados_volta = 0
        self.caminhoes_atravessados_ida = 0
        self.caminhoes_atravessados_volta = 0
        self.sentido_atual = "ida"

    def atravessar(self, carro):
        self.mutex.acquire()

        while (
            self.carros_na_ponte >= self.max_carros_na_ponte or
            self.caminhoes_na_ponte > 0 or
            self.sentido_atual != carro.sentido or
            self.carros_atravessados_ida == self.P or
            self.carros_atravessados_volta == self.P or
            self.caminhoes_atravessados_ida == self.U or
            self.caminhoes_atravessados_volta == self.U
        ):
            self.condicao.wait()

        self.carros_na_ponte += 1
        if carro.sentido == "ida":
            self.carros_atravessados_ida += 1
        else:
            self.carros_atravessados_volta += 1

        if (
            self.carros_atravessados_ida == self.P and
            self.sentido_atual == "ida"
        ):
            self.sentido_atual = "volta"
            self.carros_atravessados_ida = 0
        elif (
            self.carros_atravessados_volta == self.P and
            self.sentido_atual == "volta"
        ):
            self.sentido_atual = "ida"
            self.carros_atravessados_volta = 0

        self.condicao.notifyAll()
        self.mutex.release()

        print(f"Carro {carro.identificador} atravessando a ponte no sentido {carro.sentido}")
        tempo_inicial = time.time()
        time.sleep(Tc)
        tempo_final = time.time()
        print(f"Carro {carro.identificador} atravessou a ponte no sentido {carro.sentido}")

        self.mutex.acquire()
        self.carros_na_ponte -= 1
        if carro.sentido == "ida":
            self.carros_cruzados_ida += 1
        else:
            self.carros_cruzados_volta += 1
        self.tempo_espera_total += tempo_inicial - (carro.identificador * Ta_max)
        self.tempo_utilizacao_ponte += tempo_final - tempo_inicial
        self.tempo_total += tempo_final - (carro.identificador * Ta_max)

        self.condicao.notifyAll()
        self.mutex.release()

    def atravessar_caminhao(self, caminhao):
        self.mutex.acquire()

        while (
            self.carros_na_ponte > 0 or
            self.caminhoes_na_ponte > 0 or
            self.sentido_atual != caminhao.sentido
        ):
            self.condicao.wait()

        self.caminhoes_na_ponte += 1
        if caminhao.sentido == "ida":
            self.caminhoes_atravessados_ida += 1
        else:
            self.caminhoes_atravessados_volta += 1

        if (
            self.caminhoes_atravessados_ida == self.U and
            self.sentido_atual == "ida"
        ):
            self.sentido_atual = "volta"
            self.caminhoes_atravessados_ida = 0
        elif (
            self.caminhoes_atravessados_volta == self.U and
            self.sentido_atual == "volta"
        ):
            self.sentido_atual = "ida"
            self.caminhoes_atravessados_volta = 0

        self.condicao.notifyAll()
        self.mutex.release()

        print(f"Caminhão {caminhao.identificador} atravessando a ponte no sentido {caminhao.sentido}")
        tempo_inicial = time.time()
        time.sleep(Tt)
        tempo_final = time.time()
        print(f"Caminhão {caminhao.identificador} atravessou a ponte no sentido {caminhao.sentido}")

        self.mutex.acquire()
        self.caminhoes_na_ponte -= 1
        if caminhao.sentido == "ida":
            self.caminhoes_cruzados_ida += 1
        else:
            self.caminhoes_cruzados_volta += 1
        self.tempo_espera_total += tempo_inicial - (caminhao.identificador * Ta_max)
        self.tempo_utilizacao_ponte += tempo_final - tempo_inicial
        self.tempo_total += tempo_final - (caminhao.identificador * Ta_max)

        self.condicao.notifyAll()
        self.mutex.release()


n = 100
m = 10
Ta_min = 1
Ta_max = 3
Tc = 5
Tt = 10
Ts = 1
P = 5
U = 1

carros = []
caminhoes = []

ponte = Ponte(P, U)

for i in range(n):
    sentido = "ida" if i < n / 2 else "volta"
    if i < m:
        caminhoes.append(Caminhao(i+1, sentido, ponte))
    else:
        carros.append(Carro(i+1, sentido, ponte))

for caminhao in caminhoes:
    caminhao.start()

for carro in carros:
    carro.start()

for caminhao in caminhoes:
    caminhao.join()

for carro in carros:
    carro.join()

tempo_medio_espera = ponte.tempo_espera_total / (n + m)
tempo_utilizacao_ponte = ponte.tempo_utilizacao_ponte / ponte.tempo_total

print(f"Carros cruzados no sentido ida: {ponte.carros_cruzados_ida}")
print(f"Carros cruzados no sentido volta: {ponte.carros_cruzados_volta}")
print(f"Caminhões cruzados no sentido ida: {ponte.caminhoes_cruzados_ida}")
print(f"Caminhões cruzados no sentido volta: {ponte.caminhoes_cruzados_volta}")
print(f"Tempo mínimo de espera: {min(tempo_espera_carros)} segundos")
print(f"Tempo máximo de espera: {max(tempo_espera_carros)} segundos")
print(f"Tempo médio de espera: {tempo_medio_espera} segundos")
print(f"Tempo de utilização da ponte: {tempo_utilizacao_ponte * 100}%")
