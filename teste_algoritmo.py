from WazeRouteCalculator import WazeRouteCalculator, WRCError

"""
    Deverá terminar lógica do algoritmo, implementando:
        - Cálculo de melhor rota
        - Realizar testes (Fazendo a execução do algoritmo)
"""

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
                    rota = WazeRouteCalculator(origem, destino, region='BR')

                    _, distancia = rota.calc_route_info() # Uso do _ para ignorar a variável tempo da biblioteca
                    matriz[origem][destino] = distancia

                    print(f"{origem} -> {destino}: {distancia} km")


                except WRCError as e:
                    print(f"Erro calculando {origem} -> {destino}: {str(e)}")
                    matriz[origem][destino] = float('inf')


    return matriz