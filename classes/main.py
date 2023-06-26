from ponte import Ponte
from carros import Carro
from caminhao import Caminhao



n = 100  # número de carros
m = 10  # número de caminhões
Tc = 5  # tempo de travessia do carro
Tt = 10  # tempo de travessia do caminhão
Ts = 1  # tempo mínimo de espera entre veículos no mesmo sentido
P = 5

ponte = Ponte(P, Tc, Tt, Ts)

veiculos = []
for i in range(n):
    veiculos.append(Carro(i+1, "ida" if i < n/2 else "volta", ponte))

for i in range(m):
    veiculos.append(Caminhao(i+1, "ida" if i < m/2 else "volta", ponte))

for veiculo in veiculos:
    veiculo.start()

for veiculo in veiculos:
    veiculo.join()

tempo_medio_espera = ponte.tempo_espera_total / (n + m)
tempo_utilizacao_ponte = ponte.tempo_utilizacao_ponte / ponte.tempo_total

print(10 * "=", "Estatisticas", 10 * "=")
print(f"Quantidade de carros que cruzaram no sentido ida: {ponte.carros_cruzados_ida}")
print(f"Quantidade de carros que cruzaram no sentido volta: {ponte.carros_cruzados_volta}")
print(f"Quantidade de caminhões que cruzaram no sentido ida: {ponte.caminhoes_cruzados_ida}")
print(f"Quantidade de caminhões que cruzaram no sentido volta: {ponte.caminhoes_cruzados_volta}")
print(f"Tempo mínimo de espera na fila: {ponte.tempo_espera_total} segundos")
print(f"Tempo máximo de espera na fila: {ponte.tempo_espera_total + Tc} segundos")
print(f"Tempo médio de espera na fila: {tempo_medio_espera} segundos")
print(f"Tempo de utilização da ponte: {tempo_utilizacao_ponte * 100:.2f}%")
