# importa a biblioteca requests para fazer chamadas http na api da wikipedia
import requests

# a wikipedia pede que toda requisicao se identifique com um nome
cabecalhoRequisicao = {"User-Agent": "f1weather-trabalho-sistemas-distribuidos"}

# dicionario que guarda respostas ja buscadas para nao repetir chamadas na api
memoriaWikipedia = {}

# dicionario que traduz o nome do pais da api da f1 para a sigla usada nas bandeiras
siglasPaises = {
    "Australia": "au", "China": "cn", "Japan": "jp", "Bahrain": "bh",
    "Saudi Arabia": "sa", "USA": "us", "United States": "us", "Italy": "it",
    "Monaco": "mc", "Spain": "es", "Canada": "ca", "Austria": "at",
    "UK": "gb", "United Kingdom": "gb", "Belgium": "be", "Hungary": "hu",
    "Netherlands": "nl", "Azerbaijan": "az", "Singapore": "sg", "Mexico": "mx",
    "Brazil": "br", "Qatar": "qa", "UAE": "ae", "United Arab Emirates": "ae",
    "Portugal": "pt", "France": "fr", "Germany": "de", "Argentina": "ar"
}


# funcao que pega o titulo da pagina a partir do link completo da wikipedia
def extrairTituloPagina(urlWikipedia):
    return urlWikipedia.split("/")[-1]


# funcao que busca o texto resumo e a imagem principal de uma pagina da wikipedia
def buscarResumoWikipedia(urlWikipedia):
    # se ja buscamos esta pagina antes devolve a resposta guardada
    if urlWikipedia in memoriaWikipedia:
        return memoriaWikipedia[urlWikipedia]

    tituloPagina = extrairTituloPagina(urlWikipedia)
    urlApiResumo = "https://en.wikipedia.org/api/rest_v1/page/summary/" + tituloPagina
    respostaResumo = requests.get(urlApiResumo, headers=cabecalhoRequisicao, timeout=10)

    # valores padrao caso a pagina nao tenha imagem ou texto
    dadosResumo = {"imagemPrincipal": "", "textoResumo": ""}

    if respostaResumo.status_code == 200:
        dadosJsonResumo = respostaResumo.json()
        dadosResumo["textoResumo"] = dadosJsonResumo.get("extract", "")
        # a imagem principal pode nao existir em algumas paginas
        if "thumbnail" in dadosJsonResumo:
            dadosResumo["imagemPrincipal"] = dadosJsonResumo["thumbnail"]["source"]

    memoriaWikipedia[urlWikipedia] = dadosResumo
    return dadosResumo


# funcao que procura a primeira foto (.jpg) da pagina do circuito na wikipedia
def buscarFotoCircuito(urlWikipedia):
    chaveMemoria = "foto-" + urlWikipedia
    if chaveMemoria in memoriaWikipedia:
        return memoriaWikipedia[chaveMemoria]

    tituloPagina = extrairTituloPagina(urlWikipedia)
    urlApiMidias = "https://en.wikipedia.org/api/rest_v1/page/media-list/" + tituloPagina
    respostaMidias = requests.get(urlApiMidias, headers=cabecalhoRequisicao, timeout=10)

    linkFotoCircuito = ""

    if respostaMidias.status_code == 200:
        for itemMidia in respostaMidias.json()["items"]:
            # pega somente fotos jpg, ignorando desenhos e logos
            if itemMidia["title"].lower().endswith(".jpg") and "srcset" in itemMidia:
                # pega a versao de maior qualidade que fica no fim da lista
                linkFotoCircuito = "https:" + itemMidia["srcset"][-1]["src"]
                break

    memoriaWikipedia[chaveMemoria] = linkFotoCircuito
    return linkFotoCircuito


# funcao que monta o link da imagem da bandeira do pais usando o site flagcdn
def buscarBandeiraPais(nomePais):
    siglaPais = siglasPaises.get(nomePais, "")
    if siglaPais == "":
        return ""
    return "https://flagcdn.com/w1280/" + siglaPais + ".png"
