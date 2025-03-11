import itertools
from WazeRouteCalculator import WazeRouteCalculator, WRCError

def obter_enderecos():
    enderecos = []

    print("\nDigite os endereços (um por linha):")
    print("Primeiro endereço: Origem")
    print("Último endereço: Destino final")
    print("Endereços intermediários: Pontos de entrega\n")
    
    while True:
        endereco = input("Endereço (deixe em branco para finalizar): ").strip()

        if not endereco:
            if len(enderecos) < 2:
                print("Necessário pelo menos origem e destino!")
                continue
            break

        enderecos.append(endereco)

    return enderecos

def calcular_matriz_distancias(enderecos):
    matriz = {}

    for origem in enderecos:
        matriz[origem] = {}

        for destino in enderecos:
            if origem == destino:
                matriz[origem][destino] = 0.0 

            else:
                try:
                    rota = WazeRouteCalculator(origem, destino, region='US') 
                    _, distancia = rota.calc_route_info() 
                    matriz[origem][destino] = distancia
                    print(f"{origem} -> {destino}: {distancia} km")

                except WRCError as e:
                    print(f"Erro calculando {origem} -> {destino}: {str(e)}")
                    matriz[origem][destino] = float('inf') 

    return matriz

def calcular_melhor_rota(matriz, enderecos):
    melhores_distancia = float('inf')
    melhor_rota = None

    
    for rota in itertools.permutations(enderecos[1:-1]):
        rota_completa = [enderecos[0]] + list(rota) + [enderecos[-1]]
        distancia_total = 0

        for i in range(len(rota_completa) - 1):
            origem = rota_completa[i]
            destino = rota_completa[i + 1]
            distancia_total += matriz[origem][destino]

        if distancia_total < melhores_distancia:
            melhores_distancia = distancia_total
            melhor_rota = rota_completa

    return melhor_rota, melhores_distancia

def main():
    enderecos = obter_enderecos()

    matriz_distancias = calcular_matriz_distancias(enderecos)
    
    melhor_rota, distancia = calcular_melhor_rota(matriz_distancias, enderecos)

    if melhor_rota:
        print("\nMelhor Rota encontrada:")

        for i in range(len(melhor_rota) - 1):
            print(f"{melhor_rota[i]} -> {melhor_rota[i + 1]}")
            
        print(f"Distância total: {distancia:.2f} km")

    else:
        print("Não foi possível calcular uma rota viável.")

if __name__ == "__main__":
    main()