from ponte import Ponte
from carros import Carro

N = 100
TC = 5
P = 5

ponte = Ponte(P)

carros = []
for i in range(N):
    sentido = "ida" if i < N / 2 else "volta"
    carros.append(Carro(i+1, sentido, ponte))
    carros[i].start()

for carro in carros:
    carro.join()

tempo_medio_espera = ponte.tempo_espera_total / N
tempo_utilizacao_ponte = ponte.tempo_utilizacao_ponte / ponte.tempo_total

print(f"Quantidade de carros que cruzaram no sentido ida: {ponte.carros_cruzados_ida}")
print(f"Quantidade de carros que cruzaram no sentido volta: {ponte.carros_cruzados_volta}")
print(f"Tempo mínimo de espera na fila: {ponte.tempo_espera_total} segundos")
print(f"Tempo máximo de espera na fila: {ponte.tempo_espera_total + TC} segundos")
print(f"Tempo médio de espera na fila: {tempo_medio_espera} segundos")
print(f"Tempo de utilização da ponte: {tempo_utilizacao_ponte * N:.2f}%")
