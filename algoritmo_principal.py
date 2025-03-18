import requests
import itertools
from geopy.geocoders import Nominatim
from dotenv import load_dotenv
import os

load_dotenv(".env")

api_key = os.getenv("API_KEY")

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

def calcular_rota_otimizada(matriz):
    num_pontos = len(matriz)
    pontos = list(range(num_pontos))
    melhor_distancia = float('inf')
    melhor_rota = None
    
    for rota in itertools.permutations(pontos[1:-1]):
        rota_completa = [pontos[0]] + list(rota) + [pontos[-1]]
        print(f"Testando rota: {rota_completa}")
        distancia_total = 0

        for i in range(len(rota_completa) - 1):
            distancia_total += matriz[rota_completa[i]][rota_completa[i + 1]]

        if distancia_total < melhor_distancia:
            melhor_distancia = distancia_total
            melhor_rota = rota_completa

    return melhor_rota, melhor_distancia

def main():
    enderecos = [
        'Av. Paulista, 1000, São Paulo, SP',
        'R. dos Eucaliptos, 870, São Paulo, SP',
        'R. José dos Santos, 45, São Bernardo do Campo, SP',
        'R. Salvador Branco de Andrade, 182 Taboão da Serra, SP',
        'Rua das Acácias, 200, São Paulo, SP',
        'Av. Faria Lima, 500, São Paulo, SP',
        'R. do Sol, 300, São Bernardo do Campo, SP',
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
        melhor_rota, distancia = calcular_rota_otimizada(matriz_distancias)

        if melhor_rota:
            print("\nMelhor rota encontrada:")

            for i in range(len(melhor_rota) - 1):
                print(f"{enderecos[melhor_rota[i]]} -> {enderecos[melhor_rota[i + 1]]}")

            print(f"Distância total: {distancia:.2f} km")

        else:
            print("Não foi possível calcular uma rota viável.")
            
    else:
        print("Erro ao obter coordenadas para os endereços.")

if __name__ == "__main__":
    main()