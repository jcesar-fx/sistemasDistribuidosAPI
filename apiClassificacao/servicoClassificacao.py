# importa a biblioteca requests para fazer chamadas http nas apis de classificacao
import requests
# importa a funcao que busca a imagem principal de uma pagina da wikipedia
from apiImagens.servicoImagensWikipedia import buscarResumoWikipedia

# dicionario com a cor oficial de cada equipe usando o id da equipe na api jolpica
coresEquipes = {
    "mercedes": "#27F4D2",
    "ferrari": "#E8002D",
    "mclaren": "#FF8000",
    "red_bull": "#3671C6",
    "rb": "#6692FF",
    "alpine": "#0093CC",
    "haas": "#B6BABD",
    "audi": "#BB0A30",
    "sauber": "#52E252",
    "williams": "#64C4FF",
    "aston_martin": "#229971",
    "cadillac": "#C9A64B"
}

# cor cinza usada quando a equipe nao esta no dicionario acima
corPadraoEquipe = "#888888"


# funcao que busca na api openf1 a foto do rosto de cada piloto
def buscarFotosPilotos():
    # endereco da api gratuita openf1 com os pilotos da ultima sessao disputada
    urlApiOpenF1 = "https://api.openf1.org/v1/drivers?session_key=latest"
    respostaOpenF1 = requests.get(urlApiOpenF1, timeout=10)

    # dicionario que liga a sigla do piloto (ex: ver) ao link da foto dele
    fotosPorSigla = {}

    # verifica se a api respondeu corretamente
    if respostaOpenF1.status_code == 200:
        for itemPiloto in respostaOpenF1.json():
            # guarda a foto usando a sigla de tres letras do piloto como chave
            fotosPorSigla[itemPiloto["name_acronym"]] = itemPiloto["headshot_url"]

    return fotosPorSigla


# funcao que busca a classificacao atual do campeonato de pilotos
def buscarClassificacaoPilotos():
    urlApiPilotos = "https://api.jolpi.ca/ergast/f1/current/driverStandings.json"
    respostaApiPilotos = requests.get(urlApiPilotos, timeout=10)

    listaClassificacaoPilotos = []

    if respostaApiPilotos.status_code == 200:
        # busca as fotos dos pilotos na segunda api (openf1)
        fotosPorSigla = buscarFotosPilotos()

        # navega no json ate a lista de pilotos classificados
        dadosJsonPilotos = respostaApiPilotos.json()
        listaPilotosApi = dadosJsonPilotos["MRData"]["StandingsTable"]["StandingsLists"][0]["DriverStandings"]

        for itemPiloto in listaPilotosApi:
            dadosPiloto = itemPiloto["Driver"]
            # o piloto pode ter mudado de equipe, entao pegamos a ultima equipe da lista
            dadosEquipe = itemPiloto["Constructors"][-1]
            idEquipe = dadosEquipe["constructorId"]
            siglaPiloto = dadosPiloto.get("code", "")

            listaClassificacaoPilotos.append({
                "posicao": itemPiloto["position"],
                "nomePiloto": dadosPiloto["givenName"] + " " + dadosPiloto["familyName"],
                "siglaPiloto": siglaPiloto,
                "nomeEquipe": dadosEquipe["name"],
                "pontos": itemPiloto["points"],
                "vitorias": itemPiloto["wins"],
                "fotoPiloto": fotosPorSigla.get(siglaPiloto, ""),
                "corEquipe": coresEquipes.get(idEquipe, corPadraoEquipe)
            })

    return listaClassificacaoPilotos


# funcao que busca a classificacao atual do campeonato de construtores
def buscarClassificacaoConstrutores():
    urlApiConstrutores = "https://api.jolpi.ca/ergast/f1/current/constructorStandings.json"
    respostaApiConstrutores = requests.get(urlApiConstrutores, timeout=10)

    listaClassificacaoConstrutores = []

    if respostaApiConstrutores.status_code == 200:
        dadosJsonConstrutores = respostaApiConstrutores.json()
        listaEquipesApi = dadosJsonConstrutores["MRData"]["StandingsTable"]["StandingsLists"][0]["ConstructorStandings"]

        for itemEquipe in listaEquipesApi:
            dadosEquipe = itemEquipe["Constructor"]
            idEquipe = dadosEquipe["constructorId"]

            # usa a imagem principal da pagina da equipe na wikipedia como logo
            resumoEquipe = buscarResumoWikipedia(dadosEquipe["url"])

            listaClassificacaoConstrutores.append({
                "posicao": itemEquipe["position"],
                "nomeEquipe": dadosEquipe["name"],
                "pontos": itemEquipe["points"],
                "logoEquipe": resumoEquipe["imagemPrincipal"],
                "corEquipe": coresEquipes.get(idEquipe, corPadraoEquipe)
            })

    return listaClassificacaoConstrutores
