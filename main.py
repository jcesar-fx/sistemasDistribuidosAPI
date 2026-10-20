# importa a biblioteca os para ler a porta do servidor caso esteja hospedado online
import os
# importa a aplicacao flask configurada dentro da pasta back
from back.rotasServidor import aplicacaoFlask

# verifica se este arquivo main.py foi executado diretamente pelo comando python
if __name__ == "__main__":
    # define a porta padrao 2000 para rodar no computador ou pega a porta da hospedagem
    portaServidor = int(os.environ.get("PORT", 2000))

    # inicia o servidor web permitindo acesso pelo navegador
    aplicacaoFlask.run(host="0.0.0.0", port=portaServidor, debug=True)
