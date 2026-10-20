# importa o framework flask e a funcao de renderizar paginas html
from flask import Flask, render_template
# importa a funcao que busca o calendario de corridas da pasta apif1
from apiF1.servicoCalendarioF1 import buscarProximasCorridas
# importa as funcoes de clima da pasta apiclima
from apiClima.servicoPrevisaoTempo import buscarPrevisaoCircuito, buscarClimaAtual
# importa as funcoes de classificacao dos campeonatos
from apiClassificacao.servicoClassificacao import buscarClassificacaoPilotos, buscarClassificacaoConstrutores
# importa as funcoes que buscam imagens do circuito e bandeira
from apiImagens.servicoImagensWikipedia import buscarResumoWikipedia, buscarFotoCircuito, buscarBandeiraPais

# cria a aplicacao flask apontando para as pastas de html e css dentro da pasta front
aplicacaoFlask = Flask(
    __name__,
    template_folder="../front/templates",
    static_folder="../front/static"
)


# define a rota principal do site quando o usuario acessa o endereco inicial
@aplicacaoFlask.route("/")
def exibirPaginaInicial():
    # chama a api da f1 para pegar a lista das proximas corridas
    listaProximasCorridas = buscarProximasCorridas()

    # para cada corrida busca a previsao do tempo para o dia da prova
    for itemCorrida in listaProximasCorridas:
        itemCorrida["dadosClima"] = buscarPrevisaoCircuito(
            itemCorrida["latitudeCircuito"],
            itemCorrida["longitudeCircuito"],
            itemCorrida["dataCorridaOriginal"]
        )

    # separa a proxima corrida (destaque) das demais corridas
    proximaCorrida = None
    outrasCorridas = []
    if len(listaProximasCorridas) > 0:
        proximaCorrida = listaProximasCorridas[0]
        outrasCorridas = listaProximasCorridas[1:]

        # busca os dados extras somente para a corrida em destaque
        resumoCircuito = buscarResumoWikipedia(proximaCorrida["urlWikipediaCircuito"])
        proximaCorrida["imagemLayout"] = resumoCircuito["imagemPrincipal"]
        proximaCorrida["textoResumo"] = resumoCircuito["textoResumo"]
        proximaCorrida["fotoCircuito"] = buscarFotoCircuito(proximaCorrida["urlWikipediaCircuito"])
        proximaCorrida["bandeiraPais"] = buscarBandeiraPais(proximaCorrida["nomePais"])
        proximaCorrida["climaAtual"] = buscarClimaAtual(
            proximaCorrida["latitudeCircuito"],
            proximaCorrida["longitudeCircuito"]
        )

    # busca as classificacoes dos campeonatos de pilotos e construtores
    listaClassificacaoPilotos = buscarClassificacaoPilotos()
    listaClassificacaoConstrutores = buscarClassificacaoConstrutores()

    # a cor de destaque do site e a cor da equipe do lider do campeonato de pilotos
    corDestaque = "#E10600"
    if len(listaClassificacaoPilotos) > 0:
        corDestaque = listaClassificacaoPilotos[0]["corEquipe"]

    # envia todos os dados tratados para o arquivo html exibir na tela
    return render_template(
        "paginaInicial.html",
        proximaCorrida=proximaCorrida,
        outrasCorridas=outrasCorridas,
        listaClassificacaoPilotos=listaClassificacaoPilotos,
        listaClassificacaoConstrutores=listaClassificacaoConstrutores,
        corDestaque=corDestaque
    )
