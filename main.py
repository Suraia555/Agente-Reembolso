import os
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from supabase import create_client, Client
from openai import OpenAI
from fastapi import UploadFile, File
import csv
import codecs

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

# 💳 ROTA WEB 5: CHECKOUT AUTOMATIZADO GLOBAL (INTEGRAÇÃO PAYONEER DIRETA VIA LEMON SQUEEZY)
@app.get("/faturamento/checkout")
def gerar_checkout_automatico(token_usuario: str, valor_frete_recuperado: float):
    try:
        # 1. Valida o utilizador na Supabase via UUID
        usuario_atual = supabase.auth.get_user(token_usuario)
        uuid_cliente = usuario_atual.user.id
        
        # 2. Calcula os 20% de comissão automática
        comissao = valor_frete_recuperado * 0.20
        
        # 3. Gera o link de pagamento exclusivo do Lemon Squeezy em linha contínua
        link_pagamento_global = f"https://lemonsqueezy.com{comissao:.2f}&custom_id={uuid_cliente}"
        
        # 4. Devolve a ordem de bloqueio/cobrança para a interface do site
        return {
            "bloqueado": True,
            "motivo": "Aguardando pagamento de comissão de reembolso logístico",
            "valor_comissao_usd": f"$ {comissao:.2f} USD",
            "url_checkout": link_pagamento_global
        }
        
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Erro de cibersegurança: {e}")
# 💳 ROTA WEB 6: WEBHOOK OFICIAL LEMON SQUEEZY (LIBERAÇÃO AUTOMÁTICA NA SUPABASE)
@app.post("/webhook/lemonsqueezy")
async def receber_notificacao_pagamento_lemon(request: Request):
    try:
        # 1. Captura os dados brutos enviados pelo servidor da Lemon Squeezy
        dados_brutos = await request.body()
        
        # 2. Transforma o sinal de rede em um dicionário Python legível
        import json
        payload = json.loads(dados_brutos)
        
        # 3. LÓGICA DE LIBERAÇÃO: Verifica se o evento recebido é de uma ordem de pagamento concluída
        event_name = payload.get("meta", {}).get("event_name")
        
        if event_name == "order_created":
            # Recupera o ID único (UUID) do usuário que amarramos na linha 118 no momento do checkout
            uuid_cliente = payload.get("data", {}).get("attributes", {}).get("custom_data", {}).get("user_id")
            
            if uuid_cliente:
                print(f"🍋 Lemon Squeezy: Pagamento Confirmado para o usuário UUID: {uuid_cliente}")
                
                # 4. Atualiza a tabela na nuvem da Supabase para liberar o robô instantaneamente
                supabase.table("encomendas").update({"status_pagamento": "PAGO"}).eq("user_id", uuid_cliente).execute()
                
                return {"sucesso": True, "mensagem": "Acesso liberado automaticamente via Lemon Squeezy!"}
                
        return {"status": "Evento Lemon Squeezy recebido com sucesso."}
        
    except Exception as e:
        # Escudo de proteção try/except ativo para segurança de transações
        return {"sucesso": False, "erro_webhook_financeiro": str(e)}

# 🛍️ ROTA WEB 7: UPLOAD E PROCESSAMENTO AUTOMÁTICO DO CSV DA SHOPIFY
@app.post("/upload/csv")
async def receber_csv_shopify(token_usuario: str, file: UploadFile = File(...)):
    try:
        # 1. Valida a sessão do utilizador na nuvem via UUID para cibersegurança
        usuario_atual = supabase.auth.get_user(token_usuario)
        uuid_cliente = usuario_atual.user.id
        
        # 2. Lê o arquivo CSV enviado pelo navegador na memória RAM
        arquivo_csv = csv.reader(codecs.iterdecode(file.file, 'utf-8'))
        
        # Pula a primeira linha do cabeçalho do arquivo Shopify
        cabecalho = next(arquivo_csv)
        
        lista_encomendas_novas = []
        
        # 3. Varre o arquivo caçando os códigos de rastreio e transportadoras
        for linha in arquivo_csv:
            if len(linha) >= 3:
                codigo = linha[0].strip()
                transportadora = linha[1].strip()
                
                # Monta a estrutura técnica vinculando o dado ao UUID do dono da loja
                encomenda = {
                    "user_id": uuid_cliente,
                    "codigo_rastreio": codigo,
                    "transportadora": transportadora,
                    "status": "ELEGÍVEL PARA REEMBOLSO"
                }
                lista_encomendas_novas.append(encomenda)
        
        # 4. Faz o Bulk Insert (Envio em Massa) direto para a nuvem da Supabase
        if lista_encomendas_novas:
            supabase.table("encomendas").insert(lista_encomendas_novas).execute()
            
        return {
            "sucesso": True,
            "mensagem": f"Ficheiro processado! {len(lista_encomendas_novas)} encomendas da Shopify foram importadas com segurança.",
            "proprietario_uuid": uuid_cliente
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao processar o arquivo CSV da Shopify: {e}")

# Força a exposição da variável para a Vercel Serverless Architecture
app = app