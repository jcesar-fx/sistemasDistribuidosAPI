# importa a biblioteca requests para fazer chamadas http na api de clima
import requests

# endereco da api gratuita open-meteo que nao precisa de chave de acesso
urlApiClima = "https://api.open-meteo.com/v1/forecast"

# dicionario que traduz o codigo de tempo da open-meteo para texto e icone
descricoesTempo = {
    0: ("Céu limpo", "☀️"), 1: ("Poucas nuvens", "🌤️"), 2: ("Parcialmente nublado", "⛅"),
    3: ("Nublado", "☁️"), 45: ("Neblina", "🌫️"), 48: ("Neblina", "🌫️"),
    51: ("Garoa fraca", "🌦️"), 53: ("Garoa", "🌦️"), 55: ("Garoa forte", "🌦️"),
    61: ("Chuva fraca", "🌧️"), 63: ("Chuva", "🌧️"), 65: ("Chuva forte", "🌧️"),
    80: ("Pancadas de chuva", "🌦️"), 81: ("Pancadas de chuva", "🌧️"), 82: ("Temporal", "⛈️"),
    95: ("Trovoadas", "⛈️"), 96: ("Trovoadas com granizo", "⛈️"), 99: ("Trovoadas com granizo", "⛈️")
}


# funcao que busca o clima de agora no circuito (temperatura, vento, umidade)
def buscarClimaAtual(latitudeCircuito, longitudeCircuito):
    parametrosRequisicao = {
        "latitude": latitudeCircuito,
        "longitude": longitudeCircuito,
        "current": "temperature_2m,apparent_temperature,relative_humidity_2m,wind_speed_10m,weather_code",
        "timezone": "auto"
    }

    # valores padrao caso a api nao responda
    dadosClimaAtual = {
        "temperaturaAtual": "--", "sensacaoTermica": "--", "umidadeAr": "--",
        "velocidadeVento": "--", "descricaoTempo": "Indisponível", "iconeTempo": "❔"
    }

    respostaApiClima = requests.get(urlApiClima, params=parametrosRequisicao, timeout=10)

    if respostaApiClima.status_code == 200:
        dadosAtuais = respostaApiClima.json()["current"]
        descricaoTempo, iconeTempo = descricoesTempo.get(dadosAtuais["weather_code"], ("Indefinido", "❔"))
        dadosClimaAtual = {
            "temperaturaAtual": round(dadosAtuais["temperature_2m"]),
            "sensacaoTermica": round(dadosAtuais["apparent_temperature"]),
            "umidadeAr": dadosAtuais["relative_humidity_2m"],
            "velocidadeVento": round(dadosAtuais["wind_speed_10m"]),
            "descricaoTempo": descricaoTempo,
            "iconeTempo": iconeTempo
        }

    return dadosClimaAtual


# funcao que busca a previsao do tempo usando a latitude e a longitude do circuito
def buscarPrevisaoCircuito(latitudeCircuito, longitudeCircuito, dataCorridaOriginal):
    # parametros enviados na requisicao com as coordenadas do autodromo
    parametrosRequisicao = {
        "latitude": latitudeCircuito,
        "longitude": longitudeCircuito,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max,weather_code",
        "timezone": "auto",
        "forecast_days": 16
    }

    # valores padrao caso a api demore ou nao retorne dados
    dadosClimaTratados = {
        "temperaturaMaxima": "--",
        "temperaturaMinima": "--",
        "probabilidadeChuva": 0,
        "iconeTempo": "❔",
        "tipoPrevisao": "Dados indisponíveis no momento",
        "condicaoPista": "Sem informações da pista"
    }

    # faz a requisicao get para a api open-meteo passando os parametros
    respostaApiClima = requests.get(urlApiClima, params=parametrosRequisicao, timeout=10)

    # verifica se a resposta da api de clima deu certo com codigo 200
    if respostaApiClima.status_code == 200:
        # pega o bloco de dados diarios dentro do json retornado
        dadosDiarios = respostaApiClima.json()["daily"]
        listaDatasPrevisao = dadosDiarios["time"]

        # verifica se a data da corrida ja esta dentro dos proximos 16 dias de previsao
        if dataCorridaOriginal in listaDatasPrevisao:
            # pega a posicao exata do dia da corrida na lista de datas
            indiceDiaEscolhido = listaDatasPrevisao.index(dataCorridaOriginal)
            textoTipoPrevisao = "Previsão para o dia da corrida"
        else:
            # se a corrida for muito longe pega o clima de hoje no circuito na posicao zero
            indiceDiaEscolhido = 0
            textoTipoPrevisao = "Clima de hoje (corrida a mais de 16 dias)"

        # extrai as temperaturas e a chance de chuva na posicao escolhida
        temperaturaMaxima = dadosDiarios["temperature_2m_max"][indiceDiaEscolhido]
        temperaturaMinima = dadosDiarios["temperature_2m_min"][indiceDiaEscolhido]
        probabilidadeChuva = dadosDiarios["precipitation_probability_max"][indiceDiaEscolhido]
        codigoTempo = dadosDiarios["weather_code"][indiceDiaEscolhido]

        # se a api retornar vazio na probabilidade de chuva coloca zero por seguranca
        if probabilidadeChuva is None:
            probabilidadeChuva = 0

        # define a situacao provavel da pista de acordo com a porcentagem de chuva
        if probabilidadeChuva >= 50:
            textoCondicaoPista = "Alta chance de chuva (possível uso de pneus de chuva)"
        elif probabilidadeChuva >= 25:
            textoCondicaoPista = "Tempo instável (chance moderada de pista úmida)"
        else:
            textoCondicaoPista = "Tempo firme (provável corrida em pista seca)"

        # atualiza o dicionario com todos os dados de clima tratados
        dadosClimaTratados = {
            "temperaturaMaxima": round(temperaturaMaxima),
            "temperaturaMinima": round(temperaturaMinima),
            "probabilidadeChuva": probabilidadeChuva,
            "iconeTempo": descricoesTempo.get(codigoTempo, ("", "❔"))[1],
            "tipoPrevisao": textoTipoPrevisao,
            "condicaoPista": textoCondicaoPista
        }

    # retorna o dicionario com a previsao tratada para o servidor
    return dadosClimaTratados
