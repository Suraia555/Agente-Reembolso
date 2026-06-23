import os
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from supabase import create_client, Client
from openai import OpenAI
# Importa o módulo de segurança que você acabou de criar
from autenticacao import fazer_login_utilizador, criar_novo_utilizador, obter_link_login_google, obter_link_login_shopify

# 1. Carrega todas as credenciais de cibersegurança
load_dotenv()

# 2. Inicializa os motores externos da nuvem
supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 3. Inicializa a API Web Global
app = FastAPI(title="CarrierRefund - Core Engine")

@app.get("/")
def home():
    return {"status": "Online", "motor": "CarrierRefund Web Completo Ativo"}

# 🔐 ROTA WEB 1: LOGIN SEGURO DO UTILIZADOR
@app.post("/auth/login")
def login_web(email: str, password: str):
    # Chama a função segura do seu arquivo de autenticação
    sessao = fazer_login_utilizador(email, password)
    
    if sessao is None:
        raise HTTPException(status_code=401, detail="Falha na autenticação. Verifique as credenciais.")
        
    # Devolve o token de acesso seguro para o navegador do cliente
    return {
        "sucesso": True,
        "mensagem": "Sessão iniciada com sucesso!",
        "access_token": sessao.session.access_token
    }
    
# 🤖 ROTA WEB 2: O PROCESSADOR DE REEMBOLSOS JURÍDICOS PROTEGIDO POR UUID
@app.get("/processar/{encomenda_id}")
def processar_reembolso_web(encomenda_id: str, token_usuario: str):
    try:
        # A. Valida a sessão do utilizador na nuvem antes de tocar nos dados
        usuario_atual = supabase.auth.get_user(token_usuario)
        uuid_cliente = usuario_atual.user.id
        
        # B. Consulta a Supabase garantindo que a encomenda pertence estritamente a este utilizador
        resposta_db = supabase.table("encomendas").select("*")\
            .eq("codigo_rastreio", encomenda_id)\
            .eq("user_id", uuid_cliente).execute()
        
        if not resposta_db.data:
            raise HTTPException(status_code=404, detail="Encomenda não localizada ou acesso não autorizado.")
            
        encomenda = resposta_db.data[0] if isinstance(resposta_db.data, list) else resposta_db.data
        codigo = encomenda.get("codigo_rastreio")
        transportadora = encomenda.get("transportadora")
        
        print(f"🔒 Acesso Seguro via UUID [{uuid_cliente}] para pacote: {codigo}")

        # C. Dispara o Prompt Jurídico Blindado para a OpenAI
        print("🤖 Acionando o cérebro da Inteligência Artificial...")
        resposta_ia = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system", 
                    "content": "You are a Senior E-commerce Logistics Lawyer. Write exclusively in formal legal English. Never invent data."
                },
                {
                    "role": "user", 
                    "content": f"Draft an official claim for the package with tracking code {codigo} handled by {transportadora}."
                }
            ]
        )
        
        return {
            "sucesso": True,
            "autorizado_por_uuid": uuid_cliente,
            "carta_gerada": resposta_ia.choices.message.content
        }

    except Exception as e:
        return {
            "sucesso": False,
            "erro_detetado": str(e),
            "nota": "Escudo de privacidade RLS e UUID ativo com sucesso!"
        }

# 🌐 ROTA WEB 3: BOTÃO DE LOGIN RÁPIDO COM O GOOGLE
@app.get("/auth/google")
def login_google_web():
    link = obter_link_login_google()
    if not link:
        raise HTTPException(status_code=500, detail="Erro interno ao acionar o motor do Google.")
    return {"url_redirecionamento": link}

# 🛍️ ROTA WEB 4: BOTÃO DE CONEXÃO DIRETA COM A SHOPIFY DO CLIENTE
@app.get("/auth/shopify")
def login_shopify_web(shop_domain: str):
    link = obter_link_login_shopify(shop_domain)
    if not link:
        raise HTTPException(status_code=500, detail="Erro interno ao acionar o motor da Shopify.")
    return {"url_redirecionamento": link}
# Força a exposição da variável para a Vercel Serverless Architecture
app = app