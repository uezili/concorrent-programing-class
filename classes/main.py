from Carros import Carro
from Ponte import Ponte

n = 50
Ta_min = 1
Ta_max = 3
Tc = 5
Ts = 1

ponte = Ponte()

carros = []
for i in range(n):
    sentido = "ida" if i < n/2 else "volta"
    carros.append(Carro(i+1, sentido, ponte))
    carros[i].start()

for carro in carros:
    carro.join()

tempo_medio_espera = ponte.tempo_espera_total / n
tempo_utilizacao_ponte = ponte.tempo_utilizacao_ponte / ponte.tempo_total

print(
    f"Quantidade de carros que cruzaram no sentido ida: {ponte.carros_cruzados_ida}")
print(
    f"Quantidade de carros que cruzaram no sentido volta: {ponte.carros_cruzados_volta}")
print(f"Tempo mínimo de espera na fila: {ponte.tempo_espera_total} segundos")
print(
    f"Tempo máximo de espera na fila: {ponte.tempo_espera_total + Tc} segundos")
print(f"Tempo médio de espera na fila: {tempo_medio_espera} segundos")
print(f"Tempo de utilização da ponte: {tempo_utilizacao_ponte * n:.2f}%")
