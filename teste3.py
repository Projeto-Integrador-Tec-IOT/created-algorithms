import requests
from geopy.geocoders import Nominatim

api_key = 'INSIRA API KEY AQUI'

def obter_coordenadas(endereco):
    geolocator = Nominatim(user_agent="rota_otimizada")
    location = geolocator.geocode(endereco)

    if location:
        return location.latitude, location.longitude
    
    else:
        return None

def calcular_distancia(ponto1, ponto2):
    url = f'https://graphhopper.com/api/1/route?point={ponto1[0]},{ponto1[1]}&point={ponto2[0]},{ponto2[1]}&type=json&locale=pt-BR&key={api_key}'
    response = requests.get(url)
    
    if response.status_code == 200:
        dados = response.json()

        if 'paths' in dados:
            return dados['paths'][0]['distance'] / 1000
        
    return float('inf')

def calcular_matriz_distancias(coordenadas):
    num_pontos = len(coordenadas)
    matriz = [[0] * num_pontos for _ in range(num_pontos)]

    for i in range(num_pontos):
        for j in range(i + 1, num_pontos):
            distancia = calcular_distancia(coordenadas[i], coordenadas[j])
            matriz[i][j] = distancia
            matriz[j][i] = distancia

    return matriz

def otimizar_rota(matriz):
    url = 'https://graphhopper.com/api/1/vrp/optimize'
    headers = {'Content-Type': 'application/json'}

    data = {
        "vehicle": [{"start": 0, "end": 3}], 
        "service": [{"location": i} for i in range(1, len(matriz) - 1)],
        "matrix": matriz
    }

    params = {'key': api_key}
    response = requests.post(url, json=data, headers=headers, params=params)

    if response.status_code == 200:
        dados = response.json()

        if 'solution' in dados:
            rota = dados['solution']['routes'][0]
            return rota['activities'], rota['route_distance'] / 1000  
        
    return None, float('inf')

def main():
    enderecos = [
        'Av. Paulista, 1000, São Paulo, SP', 
        'R. dos Eucaliptos, 870, São Paulo, SP',
        'R. São Benedito, 140, Embu das Artes',
        'R. José dos Santos, 45, São Bernardo do Campo, SP',  
    ]

    coordenadas = []

    for endereco in enderecos:
        coords = obter_coordenadas(endereco)

        if coords:
            coordenadas.append(coords)

        else:
            print(f"Erro ao obter coordenadas para: {endereco}")

    if len(coordenadas) == len(enderecos):
        matriz_distancias = calcular_matriz_distancias(coordenadas)
        atividades, distancia = otimizar_rota(matriz_distancias)

        if atividades:
            print("\nMelhor rota encontrada:")

            for atividade in atividades:
                print(f"{enderecos[atividade['location']]} - {atividade['arrival']}")

            print(f"Distância total: {distancia:.2f} km")

        else:
            print("Não foi possível calcular uma rota otimizada.")
            
    else:
        print("Erro ao obter coordenadas para os endereços.")

if __name__ == "__main__":
    main()