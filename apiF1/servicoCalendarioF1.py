# importa a biblioteca requests para fazer chamadas http na internet
import requests
# importa a classe datetime para pegar a data de hoje do computador
from datetime import datetime

# dicionario que traduz o nome das sessoes da api para portugues
nomesSessoes = {
    "FirstPractice": "Treino Livre 1",
    "SecondPractice": "Treino Livre 2",
    "ThirdPractice": "Treino Livre 3",
    "SprintQualifying": "Classificação Sprint",
    "Sprint": "Corrida Sprint",
    "Qualifying": "Classificação"
}


# funcao que transforma a data ano-mes-dia no formato brasileiro dia/mes/ano
def formatarData(dataOriginal):
    partesData = dataOriginal.split("-")
    return partesData[2] + "/" + partesData[1] + "/" + partesData[0]


# funcao que transforma o horario 20:00:00Z da api em 20:00 utc
def formatarHorario(horarioOriginal):
    return horarioOriginal[0:5] + " UTC"


# funcao que busca o calendario atual da formula 1 e retorna as proximas corridas
def buscarProximasCorridas():
    # endereco da api publica gratuita jolpica que retorna o calendario atual da f1
    urlApiCalendarioF1 = "https://api.jolpi.ca/ergast/f1/current.json"

    # faz a requisicao get para buscar os dados na api da formula 1
    respostaApiF1 = requests.get(urlApiCalendarioF1, timeout=10)

    # cria a lista vazia onde vamos guardar as corridas tratadas
    listaProximasCorridas = []

    # verifica se a resposta da api deu certo com codigo 200
    if respostaApiF1.status_code == 200:
        # converte o texto recebido da api para um dicionario python em formato json
        dadosJsonF1 = respostaApiF1.json()

        # navega dentro do dicionario json ate chegar na lista de corridas da temporada
        listaTodasCorridas = dadosJsonF1["MRData"]["RaceTable"]["Races"]

        # guarda o total de etapas da temporada para mostrar etapa x de y
        totalEtapas = len(listaTodasCorridas)

        # pega a data de hoje no formato ano-mes-dia para comparar com a data da corrida
        dataHojeTexto = datetime.now().strftime("%Y-%m-%d")

        # percorre cada corrida dentro da lista de todas as corridas da temporada
        for itemCorrida in listaTodasCorridas:
            # pega a data em que a corrida vai acontecer
            dataCorridaOriginal = itemCorrida["date"]

            # verifica se a data da corrida e maior ou igual a data de hoje
            if dataCorridaOriginal >= dataHojeTexto:
                # pega os dados do circuito e da localizacao dentro do dicionario da corrida
                dadosCircuito = itemCorrida["Circuit"]
                dadosLocalizacao = dadosCircuito["Location"]

                # monta a lista de sessoes do fim de semana (treinos, sprint e classificacao)
                listaSessoes = []
                for chaveSessao in nomesSessoes:
                    # so adiciona a sessao se ela existir nesta corrida
                    if chaveSessao in itemCorrida:
                        dadosSessao = itemCorrida[chaveSessao]
                        listaSessoes.append({
                            "nomeSessao": nomesSessoes[chaveSessao],
                            "dataSessao": formatarData(dadosSessao["date"]),
                            "horarioSessao": formatarHorario(dadosSessao.get("time", "--:--"))
                        })

                # monta um dicionario simples apenas com as informacoes uteis para o nosso site
                corridaTratada = {
                    "numeroRodada": itemCorrida["round"],
                    "totalEtapas": totalEtapas,
                    "nomeGrandePremio": itemCorrida["raceName"],
                    "nomeCircuito": dadosCircuito["circuitName"],
                    "urlWikipediaCircuito": dadosCircuito["url"],
                    "nomeCidade": dadosLocalizacao["locality"],
                    "nomePais": dadosLocalizacao["country"],
                    "latitudeCircuito": dadosLocalizacao["lat"],
                    "longitudeCircuito": dadosLocalizacao["long"],
                    "dataCorridaOriginal": dataCorridaOriginal,
                    "dataCorridaFormatada": formatarData(dataCorridaOriginal),
                    "horarioCorrida": formatarHorario(itemCorrida.get("time", "--:--")),
                    "listaSessoes": listaSessoes
                }

                # adiciona a corrida tratada na nossa lista de proximas corridas
                listaProximasCorridas.append(corridaTratada)

    # retorna a lista final com as proximas corridas para o servidor
    return listaProximasCorridas
