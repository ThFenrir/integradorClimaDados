import requests
import pandas as pd
import os

API_KEY = "749fb04c29811e3ced1e4c547f08ccbe"
CIDADES = [
    'Rio Branco', 'Maceio', 'Macapa', 'Manaus', 'Salvador', 'Fortaleza', 'Brasilia',
    'Vitoria', 'Goiania', 'Sao Luis', 'Cuiaba', 'Campo Grande', 'Belo Horizonte',
    'Belem', 'Joao Pessoa', 'Curitiba', 'Recife', 'Teresina', 'Rio de Janeiro',
    'Natal', 'Porto Alegre', 'Porto Velho', 'Boa Vista', 'Florianopolis',
    'Sao Paulo', 'Aracaju', 'Palmas'
]
ARQUIVO = "dados_clima.csv"

def coleta_dados_clima (cidade):

    LINK = f"https://api.openweathermap.org/data/2.5/weather?q={cidade},BR&appid={API_KEY}&units=metric"
    resposta = requests.get(LINK)
    dados = resposta.json()
    
    return {
        # Localização
        "cidade": dados['name'],

        # Temperaturas
        "temperatura": dados['main']['temp'],
        "sens_termica": dados['main']['feels_like'],
        "temp_min": dados['main']['temp_min'],
        "temp_max": dados['main']['temp_max'],

        # Umidade
        "umidade": dados['main']['humidity'],

        # Descrição do tempo
        "clima": dados['weather'][0]['main'],
        "descricao": dados['weather'][0]['description'],

        # Velocidade do vento
        "velo_vento": dados['wind']['speed'],
        "direcao_vento": dados['wind']['deg'],

        # Pressão atmosférica
        "pressao": dados['main']['pressure'],

        # Nível de visibilidade
        "visibilidade": dados['visibility'],

        # Horário
        "hora": pd.Timestamp.now()
    }

def coleta_dados():
    dados_clima = [coleta_dados_clima(cidade) for cidade in CIDADES]
    df = pd.DataFrame(dados_clima)
    df.to_csv("dados_clima_recente.csv", index=False)
    try:
        df_existente = pd.read_csv(ARQUIVO)
        df = pd.concat([df_existente, df])
    except FileNotFoundError:
        pass
    df.to_csv(ARQUIVO, index=False)

coleta_dados()