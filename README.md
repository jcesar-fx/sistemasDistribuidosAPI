# Calendário da Fórmula 1 e Previsão do Tempo nos Circuitos

Projeto prático desenvolvido para a disciplina de **Sistemas Distribuídos**.  
Trata-se de uma aplicação web cliente/servidor em **Python (Flask)** que consome duas APIs públicas gratuitas, trata as respostas em JSON e exibe no navegador as próximas corridas da temporada atual da Fórmula 1 junto com a previsão meteorológica de cada autódromo.

---

## 1. APIs Utilizadas (Sem necessidade de cadastro ou chave)

1. **Jolpica-F1 API (Calendário da Fórmula 1):**
   - **Endereço:** `https://api.jolpi.ca/ergast/f1/current.json`
   - **O que fornece:** Lista de corridas da temporada atual com nome do Grande Prêmio, data, nome do autódromo, cidade, país e as coordenadas geográficas (`lat` e `long`).
2. **Open-Meteo API (Previsão do Tempo):**
   - **Endereço:** `https://api.open-meteo.com/v1/forecast`
   - **O que fornece:** Recebe a `latitude` e a `longitude` de cada circuito da F1 e devolve o clima atual (temperatura, sensação, umidade, vento) e a previsão do dia da corrida (máx/mín e chance de chuva).
3. **Jolpica-F1 (Classificação):** `current/driverStandings.json` e `current/constructorStandings.json`, com as tabelas dos campeonatos de pilotos e construtores.
4. **OpenF1 API:** `https://api.openf1.org/v1/drivers?session_key=latest`, com a foto do rosto de cada piloto.
5. **Wikipedia REST API:** `page/summary` e `page/media-list`, que trazem o layout do circuito, uma foto livre (Wikimedia Commons) e os logos das equipes.
6. **flagcdn:** imagem da bandeira do país-sede (`https://flagcdn.com/w1280/us.png`).

### Visual (F1Weather)
- Tema escuro; a **cor de destaque** é a da equipe do líder do campeonato de pilotos.
- Centro: a próxima corrida em destaque (layout sobre a bandeira, detalhes e sessões) e o painel de clima com a foto do circuito ao fundo.
- Esquerda: classificação de pilotos. Direita: classificação de construtores (com as cores de cada equipe).

---

## 2. Estrutura de Pastas do Projeto

```text
sistemasDistribuidosAPI/
├── main.py                      # arquivo principal que liga o servidor flask
├── requirements.txt             # bibliotecas necessarias para rodar o sistema
├── README.md                    # guia de instalacao, execucao e hospedagem
├── AGENTS.md                    # regras e padroes de codigo do projeto
├── apiF1/
│   └── servicoCalendarioF1.py   # busca e filtra as proximas corridas na api da f1
├── apiClima/
│   └── servicoPrevisaoTempo.py  # clima atual e previsao na api open-meteo
├── apiClassificacao/
│   └── servicoClassificacao.py  # campeonatos de pilotos e construtores
├── apiImagens/
│   └── servicoImagensWikipedia.py # layout, foto, logos e bandeiras
├── back/
│   └── rotasServidor.py         # junta os dados das apis e envia para o html
└── front/
    ├── templates/
    │   └── paginaInicial.html   # pagina web que mostra os cartoes das corridas
    └── static/
        └── estiloPagina.css     # visual e cores da pagina
```

---

## 3. Como Rodar o Programa no seu Computador

### Passo 1: Instalar as dependências
Abra o terminal na pasta raiz do projeto (`sistemasDistribuidosAPI`) e execute:

```bash
pip install -r requirements.txt
```

### Passo 2: Iniciar o servidor
Execute o arquivo principal:

```bash
python main.py
```

### Passo 3: Acessar no navegador
Abra o seu navegador de internet e acesse:
- **`http://localhost:5000`** (ou `http://127.0.0.1:5000`)

---

## 4. Como Hospedar Online Gratuitamente (Exigência do Trabalho: `localhost = nota zero`)

Como o enunciado exige que o trabalho também possa ser acessado online, você tem duas formas gratuitas e rápidas:

### Opção A: Hospedagem permanente gratuita no Render.com (Recomendado para entregar o link no AVA)
1. Suba esta pasta para um repositório no seu **GitHub**.
2. Crie uma conta gratuita em [https://render.com](https://render.com) e clique em **New +** -> **Web Service**.
3. Conecte o seu repositório do GitHub.
4. Configure os campos:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn main:aplicacaoFlask`
5. Clique em **Deploy Web Service**. O Render vai gerar um link público (`https://seu-projeto.onrender.com`) que qualquer pessoa (e o professor) pode abrir direto pelo navegador.

### Opção B: Expor o seu computador na hora com Cloudflare Tunnel ou Ngrok
Se quiser gerar um link público rápido direto da sua máquina sem precisar configurar servidor na nuvem:
1. Com o `python main.py` rodando na porta `5000`, abra outro terminal.
2. Usando Ngrok: `ngrok http 5000` (gera um link público `https://....ngrok-free.app`).
