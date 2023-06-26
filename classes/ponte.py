import threading
import time
from caminhao import Caminhao
from carros import Carro
from random import choice


Ta_max = 3

class Ponte:
    def __init__(self, P, Tc, Tt, Ts):
        self.max_carros_na_ponte = 5
        self.carros_na_ponte = 0
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
        self.carros_atravessados_ida = 0
        self.carros_atravessados_volta = 0
        self.caminhoes_atravessados_ida = 0
        self.caminhoes_atravessados_volta = 0
        self.sentido_atual = choice(["ida","volta"])
        self.Tc = Tc
        self.Tt = Tt
        self.Ts = Ts

    def atravessar(self, veiculo):
        self.mutex.acquire()

        while self.carros_na_ponte >= self.max_carros_na_ponte or self.sentido_atual != veiculo.sentido:
            self.condicao.wait()

        self.carros_na_ponte += 1
        if veiculo.sentido == "ida":
            if isinstance(veiculo, Carro):
                self.carros_atravessados_ida += 1
            elif isinstance(veiculo, Caminhao):
                self.caminhoes_atravessados_ida += 1
        else:
            if isinstance(veiculo, Carro):
                self.carros_atravessados_volta += 1
            elif isinstance(veiculo, Caminhao):
                self.caminhoes_atravessados_volta += 1

        if self.carros_atravessados_ida == self.P and self.sentido_atual == "ida":
            self.sentido_atual = "volta"
            self.carros_atravessados_ida = 0
        elif self.carros_atravessados_volta == self.P and self.sentido_atual == "volta":
            self.sentido_atual = "ida"
            self.carros_atravessados_volta = 0

        time.sleep(self.Ts)

        self.condicao.notifyAll()
        self.mutex.release()

        # print(f"{veiculo.__class__.__name__} {veiculo.identificador} atravessando a ponte no sentido {veiculo.sentido}")
        tempo_inicial = time.time()
        if isinstance(veiculo, Caminhao):
            time.sleep(self.Tt)
        else:
            time.sleep(self.Tc)
        tempo_final = time.time()
        print(f"{veiculo.__class__.__name__} {'-->' if veiculo.sentido == 'ida' else '<--'} {veiculo.identificador} atravessou a ponte no sentido {veiculo.sentido}")

        self.mutex.acquire()
        self.carros_na_ponte -= 1
        if veiculo.sentido == "ida":
            if isinstance(veiculo, Carro):
                self.carros_cruzados_ida += 1
            elif isinstance(veiculo, Caminhao):
                self.caminhoes_cruzados_ida += 1
        else:
            if isinstance(veiculo, Carro):
                self.carros_cruzados_volta += 1
            elif isinstance(veiculo, Caminhao):
                self.caminhoes_cruzados_volta += 1

        self.tempo_espera_total += tempo_inicial - (veiculo.identificador * Ta_max)
        self.tempo_utilizacao_ponte += tempo_final - tempo_inicial
        self.tempo_total += tempo_final - (veiculo.identificador * Ta_max)

        self.condicao.notifyAll()
        self.mutex.release()
