import os
from dotenv import load_dotenv
from supabase import create_client, Client

# 1. Inicialização e Blindagem de Credenciais da Nuvem
load_dotenv()
supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

print("--- MÓDULO CORE LOGÍSTICO: ENCOMENDAS ATIVO ---")

# 2. FUNÇÃO 1: Persistir uma nova encomenda isolada por UUID do Utilizador
def salvar_encomenda_usuario(token_usuario: str, codigo: str, transportadora: str):
    try:
        # Recupera o UUID seguro do utilizador autenticado via Supabase Auth
        usuario = supabase.auth.get_user(token_usuario)
        uuid_cliente = usuario.user.id
        
        payload = {
            "user_id": uuid_cliente,
            "codigo_rastreio": codigo,
            "transportadora": transportadora,
            "status": "ELEGÍVEL PARA REEMBOLSO",
            "status_pagamento": "NENHUMA_COBRANÇA"
        }
        
        resposta = supabase.table("encomendas").insert(payload).execute()
        print(f"📦 Encomenda {codigo} salva com sucesso na nuvem sob o UUID: {uuid_cliente}")
        return resposta
    except Exception as e:
        print(f"❌ Erro ao salvar encomenda isolada: {e}")
        return None

# 3. FUNÇÃO 2: Atualizar os Estados Críticos e Financeiros pós-processamento
def atualizar_status_contestacao(encomenda_id: str, novo_status: str, status_financeiro: str):
    try:
        # Atualiza a tabela rastreando estritamente pelo ID primário da encomenda
        resposta = supabase.table("encomendas").update({
            "status": novo_status,
            "status_pagamento": status_financeiro
        }).eq("id", encomenda_id).execute()
        
        print(f"⚙️ Status da Encomenda ID {encomenda_id} atualizado para: {novo_status}")
        return resposta
    except Exception as e:
        print(f"❌ Erro crítico ao atualizar metadados da encomenda: {e}")
        return None
