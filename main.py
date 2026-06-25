import os
import csv
import codecs
import json
from fastapi import FastAPI, HTTPException, UploadFile, File, Request
from dotenv import load_dotenv
from supabase import create_client, Client

# Importa as funções dos teus módulos especializados
from autenticacao import fazer_login_utilizador, criar_novo_utilizador, obter_link_login_google, obter_link_login_shopify
from app import gerar_carta_contestacao_ia  # <-- Injeção do módulo utilitário de IA aqui

# 1. Carrega todas as credenciais de cibersegurança
load_dotenv()

# 2. Inicializa os motores externos da nuvem (Sem OpenAI aqui, agora está isolada no app.py!)
supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

# 3. Inicializa a API Web Global
app = FastAPI(title="CarrierRefund - Core Engine")

@app.get("/")
def home():
    return {"status": "Online", "motor": "CarrierRefund Web Completo Ativo"}


# =====================================================================
# 🔐 CAMADA 1: AUTENTICAÇÃO E SESSÃO (CICLO DE VIDA DO UTILIZADOR)
# =====================================================================

# ROTA WEB 1: REGISTO DE NOVO CLIENTE PILOTO
@app.post("/auth/signup")
def signup_web(email: str, password: str):
    resposta = criar_novo_utilizador(email, password)
    if resposta is None:
        raise HTTPException(status_code=400, detail="Erro ao criar utilizador. Verifique os dados.")
    return {
        "sucesso": True,
        "mensagem": f"Utilizador {email} cadastrado com sucesso no ecossistema!"
    }

# ROTA WEB 2: LOGIN SEGURO DO UTILIZADOR (GERAÇÃO DE TOKEN)
@app.post("/auth/login")
def login_web(email: str, password: str):
    sessao = fazer_login_utilizador(email, password)
    
    if sessao is None:
        raise HTTPException(status_code=401, detail="Falha na autenticação. Verifique as credenciais.")
        
    return {
        "sucesso": True,
        "mensagem": "Sessão iniciada com sucesso!",
        "access_token": sessao.session.access_token
    }

# ROTA WEB 3: BOTÃO DE LOGIN RÁPIDO COM O GOOGLE
@app.get("/auth/google")
def login_google_web():
    link = obter_link_login_google()
    if not link:
        raise HTTPException(status_code=500, detail="Erro interno ao acionar o motor do Google.")
    return {"url_redirecionamento": link}

# ROTA WEB 4: BOTÃO DE CONEXÃO DIRETA COM A SHOPIFY DO CLIENTE
@app.get("/auth/shopify")
def login_shopify_web(shop_domain: str):
    link = obter_link_login_shopify(shop_domain)
    if not link:
        raise HTTPException(status_code=500, detail="Erro interno ao acionar o motor da Shopify.")
    return {"url_redirecionamento": link}
# =====================================================================
# 📦 CAMADA 2: PROCESSAMENTO E INGESTÃO (CORE LOGÍSTICO)
# =====================================================================

# ROTA WEB 5: O PROCESSADOR DE REEMBOLSOS JURÍDICOS PROTEGIDO POR UUID
@app.get("/processar/{encomenda_id}")
async def processar_reembolso_web(encomenda_id: str, token_usuario: str):  # <-- Adicionado async aqui
    try:
        # A. Valida a sessão do utilizador na nuvem via UUID
        usuario_atual = supabase.auth.get_user(token_usuario)
        uuid_cliente = usuario_atual.user.id
        
        # B. Consulta a Supabase garantindo isolamento absoluto de dados
        resposta_db = supabase.table("encomendas").select("*")\
            .eq("codigo_rastreio", encomenda_id)\
            .eq("user_id", uuid_cliente).execute()
        
        if not resposta_db.data:
            raise HTTPException(status_code=404, detail="Encomenda não localizada ou acesso não autorizado.")
            
        encomenda = resposta_db.data[0] if isinstance(resposta_db.data, list) else resposta_db.data
        codigo = encomenda.get("codigo_rastreio")
        transportadora = encomenda.get("transportadora")
        
        print(f"🔒 Acesso Seguro via UUID [{uuid_cliente}] para pacote: {codigo}")

        # C. Chama o cérebro da IA isolado no app.py de forma assíncrona
        print("🤖 Acionando o módulo externo de Inteligência Artificial...")
        carta_texto = await gerar_carta_contestacao_ia(codigo, transportadora)
        
        # Escudo contra falhas internas do módulo de IA
        if "ERROR_IA_GENERATION_FAILED" in carta_texto:
            raise Exception(carta_texto)
        
        return {
            "sucesso": True,
            "autorizado_por_uuid": uuid_cliente,
            "carta_gerada": carta_texto
        }

    except Exception as e:
        return {
            "sucesso": False,
            "erro_detetado": str(e),
            "nota": "Escudo de privacidade RLS ativo."
        }

# ROTA WEB 6: UPLOAD E PROCESSAMENTO AUTOMÁTICO DO CSV DA SHOPIFY
@app.post("/upload/csv")
async def receber_csv_shopify(token_usuario: str, file: UploadFile = File(...)):
    try:
        # 1. Valida a sessão do utilizador na nuvem via UUID
        usuario_atual = supabase.auth.get_user(token_usuario)
        uuid_cliente = usuario_atual.user.id
        
        # 2. Transforma o arquivo enviado em um leitor de dicionário para ignorar índices físicos
        linhas_decodificadas = codecs.iterdecode(file.file, 'utf-8')
        leitor = csv.DictReader(linhas_decodificadas)
        
        lista_encomendas_novas = []
        
        # 3. Varre o arquivo mapeando as colunas pelos nomes exatos do cabeçalho
        for linha in leitor:
            # Captura os dados blindando contra erros de chaves ausentes
            codigo = linha.get("codigo_rastreio", "").strip()
            transportadora = linha.get("transportadora", "").strip()
            
            if codigo and transportadora:
                encomenda = {
                    "user_id": uuid_cliente,
                    "codigo_rastreio": codigo,
                    "transportadora": transportadora,
                    "status": "ELEGÍVEL PARA REEMBOLSO"
                }
                lista_encomendas_novas.append(encomenda)
        
        # 4. Envio em Massa (Bulk Insert) para a nuvem da Supabase
        if lista_encomendas_novas:
            supabase.table("encomendas").insert(lista_encomendas_novas).execute()
            
        return {
            "sucesso": True,
            "mensagem": f"Ficheiro processado! {len(lista_encomendas_novas)} encomendas mapeadas com sucesso pelo cabeçalho.",
            "proprietario_uuid": uuid_cliente
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao processar o arquivo CSV da Shopify: {e}")

# =====================================================================
# 💳 CAMADA 3: PROCESSAMENTO EM LOTE E FATURAMENTO (ANTI-CALOTE)
# =====================================================================

# ROTA WEB 7: PROCESSADOR EM LOTE COM SISTEMA ANTI-CALOTE ATIVO
@app.get("/processar/lote/todas")
async def processar_todas_encomendas_usuario(token_usuario: str):
    try:
        # 1. Valida a sessão do utilizador na nuvem via UUID
        usuario_atual = supabase.auth.get_user(token_usuario)
        uuid_cliente = usuario_atual.user.id
        
        # 🚨 O ESCUDO ANTI-CALOTE: Verifica faturas marcadas como "AGUARDANDO_PAGAMENTO"
        faturas_pendentes = supabase.table("encomendas").select("id")\
            .eq("user_id", uuid_cliente)\
            .eq("status_pagamento", "AGUARDANDO_PAGAMENTO").execute()
            
        # Se o cliente tiver 3 ou mais comissões atrasadas, o robô bloqueia na hora!
        if faturas_pendentes.data and len(faturas_pendentes.data) >= 3:
            return {
                "sucesso": False,
                "bloqueado": True,
                "motivo": "Acesso suspenso por faturas de comissão pendentes.",
                "acao_requerida": "Efetue o pagamento das suas taxas de 20% na Lemon Squeezy para desbloquear o seu Agente."
            }
        
        # 2. Puxa apenas as encomendas elegíveis desse cliente específico
        resposta_db = supabase.table("encomendas").select("*")\
            .eq("user_id", uuid_cliente)\
            .eq("status", "ELEGÍVEL PARA REEMBOLSO").execute()
            
        encomendas_pendentes = resposta_db.data
        
        if not encomendas_pendentes:
            return {"sucesso": True, "mensagem": "Nenhuma encomenda pendente encontrada."}
            
        print(f"🔥 Iniciando lote automatizado: {len(encomendas_pendentes)} pacotes encontrados para o UUID {uuid_cliente}")
        
        cartas_processadas_sucesso = 0
        historico_lote = []
        
        # 3. Loop de Alto Tráfego com proteção individual (Airbag assíncrono)
        for enc in encomendas_pendentes:
            try:
                codigo = enc.get("codigo_rastreio")
                transportadora = enc.get("transportadora")
                
                # Chamada assíncrona de alta performance para o cérebro isolado no app.py
                carta_texto = await gerar_carta_contestacao_ia(codigo, transportadora)
                
                if "ERROR_IA_GENERATION_FAILED" in carta_texto:
                    raise Exception("Falha de comunicação com o motor OpenAI.")
                
                # Atualiza a encomenda marcando que a comissão de 20% entrou em modo de cobrança
                supabase.table("encomendas").update({
                    "status": "CONTESTAÇÃO DISPARADA",
                    "status_pagamento": "AGUARDANDO_PAGAMENTO"
                }).eq("id", enc.get("id")).execute()
                
                cartas_processadas_sucesso += 1
                historico_lote.append({"codigo_rastreio": codigo, "status": "Sucesso"})
                
            except Exception as erro_interno:
                historico_lote.append({
                    "codigo_rastreio": enc.get("codigo_rastreio", "Desconhecido"), 
                    "status": "Falhou",
                    "detalhe_erro": str(erro_interno)
                })
                continue
                
        return {
            "sucesso": True,
            "total_processado": cartas_processadas_sucesso,
            "resumo_execucao_lote": historico_lote
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro crítico no processamento em lote: {e}")

# ROTA WEB 8: CHECKOUT AUTOMATIZADO GLOBAL (INTEGRAÇÃO PAYONEER DIRETA VIA LEMON SQUEEZY)
@app.get("/faturamento/checkout")
def gerar_checkout_automatico(token_usuario: str, valor_frete_recuperado: float):
    try:
        # 1. Valida o utilizador na Supabase via UUID
        usuario_atual = supabase.auth.get_user(token_usuario)
        uuid_cliente = usuario_atual.user.id
        
        # 2. Calcula os 20% de comissão automática
        comissao = valor_frete_recuperado * 0.20
        
        # 3. Gera a URL vinculando o user_id nos metadados customizados para o webhook escutar
        link_pagamento_global = f"https://lemonsqueezy.com{comissao:.2f}&passthrough={uuid_cliente}"
        
        return {
            "bloqueado": True,
            "motivo": "Aguardando pagamento de comissão de reembolso logístico",
            "valor_comissao_usd": f"$ {comissao:.2f} USD",
            "url_checkout": link_pagamento_global
        }
        
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Erro de cibersegurança: {e}")

# ROTA WEB 9: WEBHOOK OFICIAL LEMON SQUEEZY (LIBERAÇÃO AUTOMÁTICA NA SUPABASE)
@app.post("/webhook/lemonsqueezy")
async def receber_notificacao_pagamento_lemon(request: Request):
    try:
        # 1. Captura os dados brutos enviados pelo servidor da Lemon Squeezy
        dados_brutos = await request.body()
        payload = json.loads(dados_brutos)
        
        event_name = payload.get("meta", {}).get("event_name")
        
        if event_name == "order_created":
            # Captura o UUID passado através do parâmetro customizado de checkout da API
            uuid_cliente = payload.get("data", {}).get("attributes", {}).get("custom_data", {}).get("user_id")
            
            # Fallback de segurança para o passthrough caso o custom_data venha estruturado diferente
            if not uuid_cliente:
                uuid_cliente = payload.get("meta", {}).get("custom_data", {}).get("passthrough") or payload.get("meta", {}).get("passthrough")
            
            if uuid_cliente:
                print(f"🍋 Lemon Squeezy: Pagamento Confirmado para o usuário UUID: {uuid_cliente}")
                
                # Atualiza a tabela na nuvem da Supabase liberando o robô instantaneamente
                supabase.table("encomendas").update({"status_pagamento": "PAGO"}).eq("user_id", uuid_cliente).execute()
                
                return {"sucesso": True, "mensagem": "Acesso liberado automaticamente via Lemon Squeezy!"}
                
        return {"status": "Evento Lemon Squeezy recebido com sucesso."}
        
    except Exception as e:
        return {"sucesso": False, "erro_webhook_financeiro": str(e)}

# Força a exposição da variável para a Vercel Serverless Architecture
app = app
