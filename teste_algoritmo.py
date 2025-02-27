from WazeRouteCalculator import WazeRouteCalculator, WRCError

def obter_localizacoes():
    # Coletando as localizações com input para testar o algoritmo
    localizacoes = []
    print("\nDigite os endereços (um por linha)")
    print("Endereço de origem: \nDestino final: \nEndereços entre origem e destino: \n")


    while True:
        # Strip para remover os espaços
        localizacao = input("Endereço (deixar em branco se tiver terminado): ").strip()

        if localizacao == False:
            if len(localizacao) < 2:
                print("Insira origem e destino por favor")
                continue

            break

        localizacoes.append(localizacao)
        return localizacoes
    
    def calc_distancias():
        matriz = {}

        for origem in localizacoes:
            matriz[origem] = {}

            for destino in localizacoes:
                # Verificação da distancia origem-destino
                if origem == destino:
                    matriz[origem][destino] == 0

                else:
                    try:
                        rota = WazeRouteCalculator(origem, destino, region='BR')
                        # _, distancia = rota.calc_route_info() testar essa linha
                        # matriz[origem][destino] = destino
                        # print(f"{origem} -> {destino}: {distancia} km")

                    except Exception as e:
                        print(f"Corrigir esse erro: {e}")

        return matriz