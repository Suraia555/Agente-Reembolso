import os
import csv
import codecs
import json
from fastapi import FastAPI, HTTPException, UploadFile, File, Request
from dotenv import load_dotenv
from supabase import create_client, Client
from autenticacao import deletar_conta_usuario_seguro
from fastapi import Header  # Para capturar o idioma do navegador de forma nativa
from tradutor_global import obter_texto_traduzido, detetar_idioma_requisicao

# Importa as funções dos teus módulos especializados
from autenticacao import (
    fazer_login_utilizador, 
    criar_novo_utilizador, 
    obter_link_login_google, 
    obter_link_login_shopify,
    solicitar_recuperacao_senha,
    confirmar_nova_senha,
    enviar_otp_login_rapido,
    verificar_otp_login_rapido
)
from app import gerar_carta_contestacao_ia
from seguranca_senhas import validar_senha_forte
from suporte_identidade import recuperar_email_via_loja_shopify, mascarar_email_privacidade
from armazenamento_perfil import gerar_url_assinada_upload, obter_avatar_perfil_seguro
from processador_webhook import processar_evento_webhook_shopify
from copiloto_suporte import executar_consulta_rag_copilot
from sucesso_cliente import calcular_nivel_tubarao, formatar_evento_live_ticker
from analise_preditiva import calcular_probabilidade_atraso_ml
from auditoria_imutavel import calcular_assinatura_bloco_ledger, gerar_certificado_selo_confianca
from seguranca_vault import encriptar_credencial_transporte, desencriptar_credencial_transporte

# Injeção dos novos cérebros de Faturamento Enterprise e Growth orgânico
from gerenciador_assinaturas import sincronizar_assinatura_e_bloqueios
from motor_afiliados import registrar_vinculo_afiliado_inicial, validar_e_disparar_cronometro_cpa

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
def login_web(email: str, password: str, accept_language: str = Header(None)):  # <-- Adicionado accept_language aqui
    # 1. Deteta automaticamente se o navegador do utilizador gringo está em en, pt, es ou fr
    idioma = detetar_idioma_requisicao(accept_language)
    
    sessao = fazer_login_utilizador(email, password)
    
    if sessao is None:
        # 2. Busca a mensagem de erro traduzida do teu arquivo 'tradutor_global.py'
        mensagem_erro = obter_texto_traduzido("erro_autenticacao", idioma)
        raise HTTPException(status_code=401, detail=mensagem_erro)
        
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
# ROTA WEB 4B: SOLICITAR LINK DE RECUPERAÇÃO DE SENHA POR EMAIL
@app.post("/auth/recuperar-senha/solicitar")
def solicitar_link_recuperacao(email: str):
    resposta = solicitar_recuperacao_senha(email)
    if resposta is None:
        raise HTTPException(status_code=400, detail="Erro ao processar pedido de recuperação.")
    return {"sucesso": True, "mensagem": f"E-mail de redefinição enviado para {email}."}

# ROTA WEB 4C: CONFIRMAR NOVA SENHA (COM ESCUDO ATIVO VIA NOVO MÓDULO)
@app.post("/auth/recuperar-senha/confirmar")
def redefinir_senha_usuario(nova_password: str):
    # 🚨 BARREIRA INDUSTRIAL: O main.py usa o seguranca_senhas antes de processar!
    if not validar_senha_forte(nova_password):
        raise HTTPException(
            status_code=400, 
            detail="A nova senha não cumpre os requisitos de cibersegurança padrão global."
        )
        
    resposta = confirmar_nova_senha(nova_password)
    if resposta is None:
        raise HTTPException(status_code=400, detail="Erro crítico ao atualizar a credencial na nuvem.")
    return {"sucesso": True, "mensagem": "Senha redefinida com sucesso no ecossistema!"}

# ROTA WEB 4D: ENVIAR LOGIN RÁPIDO SEM SENHA (OTP)
@app.post("/auth/otp/enviar")
def disparar_otp_usuario(email: str):
    resposta = enviar_otp_login_rapido(email)
    if resposta is None:
        raise HTTPException(status_code=400, detail="Erro ao gerar token de acesso rápido.")
    return {"sucesso": True, "mensagem": f"Token OTP enviado para {email}."}

# ROTA WEB 4E: VERIFICAR TOKEN DE ACESSO RÁPIDO (OTP)
@app.post("/auth/otp/verificar")
def validar_otp_usuario(email: str, token_6_digitos: str):
    sessao = verificar_otp_login_rapido(email, token_6_digitos)
    if sessao is None:
        raise HTTPException(status_code=401, detail="Token OTP inválido ou expirado.")
    return {
        "sucesso": True,
        "mensagem": "Autenticação Passwordless confirmada!",
        "access_token": sessao.session.access_token
    }

# ROTA WEB 4F: RECUPERAÇÃO DESCENTRALIZADA DE IDENTIDADE (PROVEDOR SHOPIFY)
@app.get("/auth/recuperar-email/shopify")
def recuperar_email_por_loja(dominio_shopify: str):
    # A. Executa a busca reversa utilizando o módulo especializado
    email_localizado = recuperar_email_via_loja_shopify(dominio_shopify)
    
    # B. Tratamento de exceções e escudos de infraestrutura
    if email_localizado == "LOJA_NAO_ENCONTRADA":
        raise HTTPException(
            status_code=404, 
            detail="Nenhum vínculo logístico localizado para o domínio inserido."
        )
    if email_localizado == "PERFIL_INCOMPLETO" or email_localizado.startswith("ERROR_INTERNAL"):
        raise HTTPException(
            status_code=500, 
            detail="Erro interno de sincronização na nuvem do ecossistema."
        )
        
    # C. Aplica o mascarador de privacidade padrão internacional antes de devolver ao navegador
    email_protegido = mascarar_email_privacidade(email_localizado)
    
    return {
        "sucesso": True,
        "mensagem": "Identidade localizada de forma descentralizada!",
        "loja_identificada": dominio_shopify,
        "pista_email_proprietario": email_protegido
    }
# ROTA WEB 4G: ELIMINAÇÃO DE CONTA COM ANONIMIZAÇÃO CRIPTOGRÁFICA (ANTI-CALOTE)
@app.delete("/auth/conta/eliminar")
def eliminar_conta_sistema(token_usuario: str):
    resposta = deletar_conta_usuario_seguro(token_usuario)
    if resposta is None:
        raise HTTPException(status_code=400, detail="Não foi possível processar a eliminação segura da conta.")
    return {
        "sucesso": True, 
        "mensagem": "Conta removida com sucesso. Todos os dados pessoais foram destruídos e o e-mail banido."
    }
# =====================================================================
# 📁 CAMADA 1B: GESTÃO DE PERFIL E ARMAZENAMENTO DIGITAL (CDN ECOSYSTEM)
# =====================================================================

# ROTA WEB 4H: SOLICITAR AUTORIZAÇÃO TEMPORÁRIA DE ESCREVER NO STORAGE
@app.post("/auth/perfil/avatar/upload-url")
def obter_url_upload_avatar(token_usuario: str, extensao: str = "webp"):
    resposta = gerar_url_assinada_upload(token_usuario, extensao)
    if not resposta.get("sucesso"):
        raise HTTPException(
            status_code=400, 
            detail=f"Erro de infraestrutura ao alocar espaço na nuvem: {resposta.get('erro_detetado')}"
        )
    return resposta

# ROTA WEB 4I: RECUPERAR LINK SEGURO DE LEITURA DO AVATAR VIA CDN
@app.get("/auth/perfil/avatar/visualizar")
def visualizar_avatar_perfil(token_usuario: str, caminho_remoto: str):
    link_cdn = obter_avatar_perfil_seguro(token_usuario, caminho_remoto)
    if link_cdn == "ACESSO_NEGADO":
        raise HTTPException(
            status_code=403, 
            detail="Violação de segurança: Não tem permissão para aceder a este diretório binário."
        )
    return {"sucesso": True, "url_temporaria_visualizacao": link_cdn}
# =====================================================================
# 🔐 CAMADA 1C: COFRE DE CONHECIMENTO ZERO (ZERO-KNOWLEDGE VAULT)
# =====================================================================

# ROTA WEB 4J: SALVAR E CRIPTOGRAFAR CREDENCIAL DA TRANSPORTADORA NO COFRE
@app.post("/vault/credenciais/salvar")
def salvar_credencial_no_cofre(token_usuario: str, transportadora: str, credencial_pura: str):
    try:
        # A. Valida a sessão do utilizador na nuvem via UUID
        usuario_atual = supabase.auth.get_user(token_usuario)
        uuid_cliente = usuario_atual.user.id
        
        # B. Executa o algoritmo AES-256-GCM em memória RAM isolada
        dados_cripto = encriptar_credencial_transporte(credencial_pura)
        
        if not dados_cripto.get("sucesso"):
            raise HTTPException(status_code=500, detail="Falha crítica ao executar criptografia do Vault.")
            
        # C. Persiste o bloco binário indecifrável na nuvem do Supabase sob RLS
        resposta_db = supabase.table("vault_credenciais").insert({
            "user_id": uuid_cliente,
            "transportadora": transportadora.strip(),
            "encrypted_payload": dados__cripto.get("encrypted_payload"),
            "nonce": dados__cripto.get("nonce"),
            "tag": dados__cripto.get("tag")
        }).execute()
        
        if not resposta_db.data:
            raise Exception("Erro ao gravar os binários criptográficos no banco de dados.")
            
        print(f"🔒 Vault Secure: Credencial para {transportadora} trancada sob o UUID [{uuid_cliente[:8]}].")
        return {
            "sucesso": True,
            "mensagem": f"Credencial da transportadora {transportadora} blindada com sucesso no cofre!"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro de barramento ou cibersegurança no Vault: {e}")

# ROTA WEB 4K: RECUPERAR E DECIFRAR CREDENCIAL (USADA INTERNAMENTE PELO ROBÔ DE SCRAPING)
@app.get("/vault/credenciais/recuperar")
def recuperar_credencial_do_cofre(token_usuario: str, transportadora: str):
    try:
        # A. Valida a sessão do utilizador na nuvem via UUID (Bloqueio RLS ativo)
        usuario_atual = supabase.auth.get_user(token_usuario)
        uuid_cliente = usuario_atual.user.id
        
        # B. Busca os metadados criptográficos na Supabase filtrando pelo UUID do utilizador
        resposta_db = supabase.table("vault_credenciais").select("*")\
            .eq("user_id", uuid_cliente)\
            .eq("transportadora", transportadora.strip()).execute()
            
        if not resposta_db.data:
            raise HTTPException(status_code=404, detail="Nenhuma credencial localizada para esta transportadora.")
            
        registro = resposta_db.data[0]
        
        # C. Invoca o decifrador injetando o Payload + Nonce + Tag recuperados da nuvem
        credencial_aberta = desencriptar_credencial_transporte(
            encrypted_payload=registro.get("encrypted_payload"),
            nonce_b64=registro.get("nonce"),
            tag_b64=registro.get("tag")
        )
        
        if credencial_aberta == "ERROR_VAULT_DECRYPTION_FAILED":
            raise HTTPException(status_code=400, detail="Falha catastrófica de integridade: Os dados foram corrompidos.")
            
        print(f"🔑 Vault Access: Credencial decifrada temporariamente em RAM para o robô de scraping.")
        return {
            "sucesso": True,
            "transportadora": transportadora,
            "credencial_autenticada_pura": credencial_aberta # Esta string viaja encriptada no túnel HTTPS nativo
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro crítico ao aceder ao cofre: {e}")
# =====================================================================
# 👥 CAMADA 1D: MOTOR DE CRESCIMENTO E AFILIADOS CPA (GROWTH ENGINE)
# =====================================================================

# ROTA WEB 4L: GERAR LINK PARAMETRIZADO DE AFILIADO CORPORATIVO
@app.get("/afiliados/gerar-link")
def obter_link_afiliado_customizado(token_usuario: str):
    try:
        # A. Valida a sessão do utilizador na nuvem via UUID
        usuario_atual = supabase.auth.get_user(token_usuario)
        uuid_afiliado = usuario_atual.user.id
        
        # B. Constrói o link oficial parametrizado que o lojista vai divulgar
        link_oficial = f"https://carrierrefund.com{uuid_afiliado}"
        
        print(f"👥 Growth: Link de afiliado gerado para UUID [{uuid_afiliado[:8]}].")
        return {
            "sucesso": True,
            "afiliado_uuid": uuid_afiliado,
            "link_promocional_cpa": link_oficial
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao gerar link de afiliado: {e}")

# ROTA WEB 4M: EXTRAIR MÉTRICAS DE GANHOS DO DASHBOARD (A TUA TRAVA DE 15 DIAS)
@app.get("/afiliados/painel-ganhos")
def obter_metricas_afiliados_dashboard(token_usuario: str):
    try:
        # A. Valida a sessão do utilizador na nuvem via UUID
        usuario_atual = supabase.auth.get_user(token_usuario)
        uuid_afiliado = usuario_atual.user.id
        
        # B. Busca na nuvem todas as indicações feitas por este utilizador
        resposta_db = supabase.table("parcerias_afiliados")\
            .select("status_premio, valor_usd, data_validacao_premio")\
            .eq("afiliado_id", uuid_afiliado).execute()
            
        dados = resposta_db.data or []
        
        # C. MATEMÁTICA ESTATÍSTICA DE RETENÇÃO EM MEMÓRIA RAM (15 Days Hold Filter)
        from datetime import datetime, timezone, timedelta
        
        total_indicados = len(dados)
        saldo_disponivel_saque = 0.0
        saldo_retido_janela = 0.0  # Dinheiro que fica trancado visivelmente no Dashboard!
        indicacoes_aguardando = 0
        
        data_atual_utc = datetime.now(timezone.utc)
        
        for item in dados:
            status = item.get("status_premio")
            valor = float(item.get("valor_usd", 5.00))
            data_validacao_str = item.get("data_validacao_premio")
            
            if status == "PRONTO_PARA_SAQUE" and data_validacao_str:
                # Converte a data de validação gravada na nuvem tirando o fuso horário
                data_validacao = datetime.fromisoformat(data_validacao_str.replace("Z", "+00:00"))
                
                # 🚨 A TUA TRAVA DE SEGURANÇA COMERCIAL DE 15 DIAS
                if data_atual_utc >= data_validacao + timedelta(days=15):
                    saldo_disponivel_saque += valor
                else:
                    saldo_retido_janela += valor
            elif status == "AGUARDANDO_VALIDACAO":
                indicacoes_aguardando += 1
                
        return {
            "sucesso": True,
            "afiliado_uuid": uuid_afiliado,
            "metricas": {
                "total_lojistas_indicados": total_indicados,
                "indicacoes_em_quarentena_antifraude": indicacoes_aguardando,
                "saldo_retido_em_seguranca_usd": round(saldo_retido_janela, 2), # Exibe o hold de 15 dias
                "saldo_liberado_para_saque_usd": round(saldo_disponivel_saque, 2), # Dinheiro real limpo
                "moeda": "USD"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao extrair métricas do painel de afiliados: {e}")
# ROTA WEB 4N: CONSULTAR STATUS DO PLANO, LIMITES E PRIVILÉGIOS CONTRATUAIS
@app.get("/faturamento/assinatura/status")
def obter_privilegios_e_status_plano(token_usuario: str):
    try:
        # A. Valida a sessão do utilizador na nuvem via UUID
        usuario_atual = supabase.auth.get_user(token_usuario)
        uuid_cliente = usuario_atual.user.id
        
        # B. Busca os dados de faturamento e bloqueios gravados na nuvem
        resposta_db = supabase.table("faturamento_assinaturas")\
            .select("plano_nome, status_assinatura, limite_mensal_pacotes, comissao_success_fee, acesso_motor_preditivo, acesso_ledger_blockchain")\
            .eq("user_id", uuid_cliente).execute()
            
        # C. ESTRUTURA DE FALLBACK SE FOR UM UTILIZADOR NOVO SEM ASSINATURA REGISTADA
        # Por defeito, ele nasce no plano Starter gratuito de teste
        dados_plano = {
            "plano_nome": "STARTER (NÃO ATIVADO)",
            "status_assinatura": "INATIVO",
            "limite_mensal_pacotes": 200,
            "comissao_success_fee_porcento": 20.0,
            "funcionalidades_liberadas": {
                "motor_preditivo_ml": False,
                "ledger_blockchain_imutavel": False
            }
        }
        
        if resposta_db.data and len(resposta_db.data) > 0:
            registro = resposta_db.data[0]
            dados_plano = {
                "plano_nome": registro.get("plano_nome", "STARTER"),
                "status_assinatura": registro.get("status_assinatura", "INATIVO"),
                "limite_mensal_pacotes": registro.get("limite_mensal_pacotes", 200),
                "comissao_success_fee_porcento": float(registro.get("comissao_success_fee", 20.0)),
                "funcionalidades_liberadas": {
                    "motor_preditivo_ml": bool(registro.get("acesso_motor_preditivo", False)),
                    "ledger_blockchain_imutavel": bool(registro.get("acesso_ledger_blockchain", False))
                }
            }
            
        print(f"💳 Billing: Privilégios contratuais extraídos para o cliente UUID [{uuid_cliente[:8]}].")
        return {
            "sucesso": True,
            "user_id": uuid_cliente,
            "assinatura_dashboard": dados_plano
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao extrair privilégios de faturamento: {e}")

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

# ROTA WEB 6B: WEBHOOK REAL TIME SHOPIFY (AUTOMAÇÃO INVISÍVEL DE DISPUTAS)
@app.post("/webhook/shopify/orders")
async def receber_notificacao_pedido_shopify(request: Request):
    try:
        # 1. Captura o payload bruto em JSON disparado pelos servidores da Shopify
        dados_brutos = await request.body()
        payload_shopify = json.loads(dados_brutos)
        
        # 2. Envia os dados para o módulo especializado processar autonomamente
        resultado = await processar_evento_webhook_shopify(payload_shopify)
        
        if not resultado.get("sucesso"):
            # Retorna um status 200 para a Shopify não ficar a tentar rebanhar o webhook em loop
            return {"status": "ignorado", "motivo": resultado.get("motivo")}
            
        dados_finais = resultado.get("dados_encomenda")
        
        # 3. Nota de Engenharia: Em produção, o webhook descobre o UUID do cliente 
        # cruzando o domínio da loja (X-Shopify-Shop-Domain) com a tabela de conexões.
        # Para o teste de integridade estrutural, simulamos a persistência sob RLS:
        print(f"🛒 Shopify Webhook: Pedido #{dados_finais['shopify_order_id']} mapeado e pronto para a Supabase.")
        
        return {"sucesso": True, "mensagem": "Evento da Shopify capturado e processado com soberania técnica."}
        
    except Exception as e:
        return {"sucesso": False, "erro_webhook_logistico": str(e)}

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
# =====================================================================
# 🤖 CAMADA 4: COGNITIVA E ASSISTÊNCIA DE ALTA DISPONIBILIDADE
# =====================================================================

# ROTA WEB 10: CARRIERREFUND AI COPILOT GATEWAY (SISTEMA RAG VETORIAL)
@app.post("/suporte/copilot/perguntar")
async def consultar_copiloto_inteligente(pergunta: str, token_usuario: str, accept_language: str = Header(None)):
    try:
        # A. Valida a sessão do utilizador na nuvem antes de gastar recursos da API
        usuario_atual = supabase.auth.get_user(token_usuario)
        uuid_cliente = usuario_atual.user.id
        
        # B. Deteta dinamicamente o idioma para a IA responder na língua do lojista
        idioma = detetar_idioma_requisicao(accept_language)
        
        print(f"🧠 AI Copilot: Processando consulta RAG para o UUID [{uuid_cliente}] no idioma [{idioma}].")
        
        # C. Invoca o cérebro vetorial assíncrono isolado no módulo copiloto_suporte
        resposta_assistente = await executar_consulta_rag_copilot(pergunta, idioma)
        
        if "ERROR_VECTOR_GENERATION_FAILED" in resposta_assistente or "ERROR_COPILOT_FAILED" in resposta_assistente:
            raise HTTPException(status_code=500, detail="Erro interno no motor de processamento vetorial.")
            
        return {
            "sucesso": True,
            "autorizado_por_uuid": uuid_cliente,
            "pergunta_original": pergunta,
            "resposta_copilot": resposta_assistente
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Falha de cibersegurança ou barramento RLS: {e}")
# =====================================================================
# 📈 CAMADA 5: EXPERIÊNCIA DO UTILIZADOR E RETENÇÃO (GROWTH LOGIC)
# =====================================================================

# ROTA WEB 11: CONSULTAR STATUS DE CRESCIMENTO E PRIVILÉGIOS DO CLIENTE
@app.get("/customer/gamificacao/status")
def obter_nivel_cliente(token_usuario: str):
    try:
        # 1. Valida a sessão do utilizador na nuvem via UUID
        usuario_atual = supabase.auth.get_user(token_usuario)
        uuid_cliente = usuario_atual.user.id
        
        # 2. Consulta a View de alta performance filtrando pelo UUID do utilizador
        resposta_db = supabase.table("view_volume_utilizadores")\
            .select("total_ganhas")\
            .eq("user_id", uuid_cliente).execute()
            
        total_vitorias = 0
        
        # 🛡️ CORREÇÃO DO SDK: Lê o primeiro registo da lista se houver dados
        if resposta_db.data and isinstance(resposta_db.data, list) and len(resposta_db.data) > 0:
            total_vitorias = resposta_db.data[0].get("total_ganhas", 0)
            
        # 3. Calcula as métricas em memória RAM instantaneamente usando o sucesso_cliente
        status_crescimento = calcular_nivel_tubarao(total_vitorias)
        
        return {
            "sucesso": True,
            "user_id": uuid_cliente,
            "total_reembolsos_ganhos": total_vitorias,
            "perfil_gamificado": status_crescimento
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro de infraestrutura ao computar nível: {e}")
# =====================================================================
# 🔮 CAMADA 6: INTELIGÊNCIA PREDICTIVA E ANÁLISE DE DADOS (ML LAYER)
# =====================================================================

# ROTA WEB 12: MOTOR PREDITIVO DE ATRASOS (LOGISTICS PREDICTIVE ANALYTICS)
@app.get("/analytics/preditivo/latencia")
def obter_alerta_preventivo_rota(transportadora: str, token_usuario: str, pico_sazonal: bool = False):
    try:
        # 1. Valida a sessão do utilizador na nuvem via UUID
        usuario_atual = supabase.auth.get_user(token_usuario)
        uuid_cliente = usuario_atual.user.id
        
        # 2. Consulta a View de latência na nuvem para buscar o histórico da transportadora
        # 🚨 RETIFICAÇÃO: Adicionada a coluna 'media_dias_historica' no select
        resposta_db = supabase.table("view_latencia_transportadoras")\
            .select("taxa_historica_atraso_porcento, media_dias_historica")\
            .eq("transportadora", transportadora.strip()).execute()
            
        taxa_historica = 0.0
        media_dias = 0.0  # 🚨 RETIFICAÇÃO: Variável de suporte inicial
        
        # 🛡️ O TEU ESCUDO DO SDK: Mantido 100% intacto, apenas extrai o novo dado
        if resposta_db.data and isinstance(resposta_db.data, list) and len(resposta_db.data) > 0:
            taxa_historica = float(resposta_db.data[0].get("taxa_historica_atraso_porcento", 0.0))
            media_dias = float(resposta_db.data[0].get("media_dias_historica", 0.0)) # 🚨 RETIFICAÇÃO: Captura dinâmica
            
        # 3. Invoca o cérebro matemático isolado no analise_preditiva.py
        # 🚨 RETIFICAÇÃO: Agora passa a média de dias capturada da View para o modelo de ML
        previsao = calcular_probabilidade_atraso_ml(
            taxa_historica_transportadora=taxa_historica, 
            media_dias_historica=media_dias, 
            dias_pico_sazonal=pico_sazonal
        )
        
        print(f"🔮 Predictive: Insights gerados para UUID [{uuid_cliente}] sobre a transportadora [{transportadora}].")
        
        return {
            "sucesso": True,
            "autorizado_por_uuid": uuid_cliente,
            "transportadora_analisada": transportadora,
            "taxa_base_historica_porcento": taxa_historica,
            "insights_preditivos": previsao
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro de processamento no motor de ML: {e}")
# =====================================================================
# 🔐 CAMADA 7: CONFORMIDADE, COMPLIANCE E LEDGER IMUTÁVEL (AUDIT LAYER)
# =====================================================================

# ROTA WEB 13: EMISSÃO DO SELO DE CONFIANÇA E CONSULTA DE LOG IMUTÁVEL
@app.post("/compliance/auditoria/registrar")
def registrar_e_emitir_selo_auditoria(encomenda_id: str, acao: str, token_usuario: str):
    try:
        # 1. Valida a sessão do utilizador na nuvem via UUID
        usuario_atual = supabase.auth.get_user(token_usuario)
        uuid_cliente = usuario_atual.user.id
        
        # 2. Busca o último bloco registrado desse cliente para capturar o hash_bloco_anterior
        ultimo_bloco = supabase.table("auditoria_ledger")\
            .select("hash_bloco_atual")\
            .eq("user_id", uuid_cliente)\
            .order("created_at", desc=True)\
            .limit(1).execute()
            
        hash_anterior = "0" * 64  # Hash Gênesis caso seja a primeira ação do cliente
        
        if ultimo_bloco.data and isinstance(ultimo_bloco.data, list) and len(ultimo_bloco.data) > 0:
            hash_anterior = ultimo_bloco.data[0].get("hash_bloco_atual", "0" * 64)
            
        # 3. Calcula o novo Hash encadeado (Blockchain Style) em memória RAM
        hash_atual = calcular_assinatura_bloco_ledger(hash_anterior, uuid_cliente, acao, encomenda_id)
        
        if hash_atual == "ERROR_HASH_GENERATION_FAILED":
            raise HTTPException(status_code=500, detail="Erro interno ao criptografar o bloco de auditoria.")
            
        # 4. Grava o log imutável na tabela da nuvem do Supabase
        resposta_insersao = supabase.table("auditoria_ledger").insert({
            "user_id": uuid_cliente,
            "encomenda_id": encomenda_id,
            "acao_executada": acao,
            "hash_bloco_anterior": hash_anterior,
            "hash_bloco_atual": hash_atual
        }).execute()
        
        if not resposta_insersao.data:
            raise Exception("Falha ao gravar no livro de registro digital.")
            
        id_registro = resposta_insersao.data[0].get("id")
        
        # 5. Gera o Selo de Confiança Criptográfico público para relatórios judiciais
        selo = gerar_certificado_selo_confianca(id_registro, hash_atual)
        
        print(f"🔐 Ledger: Bloco [{id_registro[:8]}] encadeado com sucesso para o UUID [{uuid_cliente}].")
        
        return {
            "sucesso": True,
            "autorizado_por_uuid": uuid_cliente,
            "acao_registrada": acao,
            "hash_bloco_encadeado": hash_atual,
            "selo_confianca_emitido": selo
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro crítico no barramento de compliance: {e}")

# Força a exposição da variável para a Vercel Serverless Architecture
app = app
