from fastapi import FastAPI

# 1. Inicializa a aplicação Web do FastAPI
app = FastAPI(title="Agente Reembolso API Global")

# 2. Criar a primeira ROTA WEB (A porta de entrada do site)
# O símbolo "@app.get('/')" diz que quando alguém acessar o link principal, esta rota responde.
@app.get("/")
def pagina_inicial():
    return {
        "status": "Online",
        "mensagem": "O motor do Agente de Reembolso está conectado à internet!",
        "mercado": "Global"
    }

# 3. Criar a rota de teste de saúde do sistema (Health Check)
@app.get("/saude")
def verificar_saude():
    return {"modulo_ia": "Pronto", "modulo_dados": "Conectado"}
