import threading
import random
import time

# Variáveis do problema
n = 100  # número total de carros
ta_min = 1  # tempo mínimo de chegada
ta_max = 3  # tempo máximo de chegada
tc = 5  # tempo de travessia
ts = 1  # espaço entre os veículos no mesmo sentido

# Variáveis para controle do número de carros na ponte
max_carros_na_ponte = 5
carros_na_ponte = 0
mutex = threading.Semaphore(1)

# Função que representa a travessia de um carro
def travessia_carro(sentido):
    global carros_na_ponte
    
    # Aguarda o espaço na ponte para atravessar
    mutex.acquire()
    while carros_na_ponte >= max_carros_na_ponte:
        mutex.release()
        time.sleep(0.1)  # Espera um tempo antes de tentar novamente
        mutex.acquire()

    # Atravessa a ponte
    carros_na_ponte += 1
    mutex.release()
    
    print(f"Carro -> {threading.current_thread().name} atravessando a ponte no sentido {sentido}")
    time.sleep(tc)
    print(f"Carro -> {threading.current_thread().name} atravessou a ponte no sentido {sentido}")

    # Libera espaço na ponte
    mutex.acquire()
    carros_na_ponte -= 1
    mutex.release()

# Função que gera os carros e inicia suas threads
def gera_carros():
    carros = []
    for i in range(n):
        sentido = "ida" if i < n/2 else "volta"
        tempo_chegada = random.uniform(ta_min, ta_max)
        
        carros.append(threading.Thread(target=travessia_carro, args=(sentido,), name=f"Carro {i+1}"))
        time.sleep(tempo_chegada)
        carros[i].start()

    # Espera todas as threads terminarem
    for carro in carros:
        carro.join()

# Executa a função principal
gera_carros()
