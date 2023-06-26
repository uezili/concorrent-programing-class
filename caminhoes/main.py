from carro import Veiculo
from ponte import Ponte


n = 100
m = 10
Ta_min = 1
Ta_max = 3
Tc = 5
Tt = 10
Ts = 1
P = 5
U = 1

ponte = Ponte(P, U)

veiculos = []
for i in range(n):
    if i < n/2:
        sentido = "ida"
        if i < m:
            veiculos.append(Veiculo(i+1, "caminhao", sentido, ponte))
        else:
            veiculos.append(Veiculo(i+1, "carro", sentido, ponte))
    else:
        sentido = "volta"
        if i >= n/2 and i < n/2 + m:
            veiculos.append(Veiculo(i+1, "caminhao", sentido, ponte))
        else:
            veiculos.append(Veiculo(i+1, "carro", sentido, ponte))
    veiculos[i].start()

for veiculo in veiculos:
    veiculo.join()

tempo_medio_espera = ponte.tempo_espera_total / (n + m)
tempo_utilizacao_ponte = ponte.tempo_utilizacao_ponte / ponte.tempo_total

print(f"Quantidade de carros que cruzaram no sentido ida: {ponte.carros_cruzados_ida}")
print(f"Quantidade de carros que cruzaram no sentido volta: {ponte.carros_cruzados_volta}")
print(f"Quantidade de caminhões que cruzaram no sentido ida: {ponte.caminhoes_atravessados_ida}")
print(f"Quantidade de caminhões que cruzaram no sentido volta: {ponte.caminhoes_atravessados_volta}")
# print(f"Tempo mínimo de espera na fila: {minimo_espera:.2f} segundos")
# print(f"Tempo máximo de espera na fila: {maximo_espera:.2f} segundos")
print(f"Tempo médio de espera na fila: {tempo_medio_espera:.2f} segundos")
print(f"Tempo de utilização da ponte: {tempo_utilizacao_ponte * 100:.2f}%")
