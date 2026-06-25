import os
from dotenv import load_dotenv
from supabase import create_client, Client

# 1. Carrega as credenciais de segurança do arquivo oculto .env
load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")

# URL de redirecionamento dinâmico para produção ou localhost
# Se não estiver no .env, usa o fallback seguro
REDIRECT_URL = os.getenv("REDIRECT_TO_URL", "https://vercel.app")

# 2. Inicializa o cliente seguro da Supabase
supabase: Client = create_client(url, key)

print("--- REQUISITO DE SEGURANÇA: MÓDULO SUPABASE AUTH ATIVADO ---")

# 3. FUNÇÃO 1: Registar um novo utilizador na nuvem
def criar_novo_utilizador(email: str, password: str):
    try:
        resposta = supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        # Verifica se a nuvem retornou algum erro interno antes de confirmar
        if hasattr(resposta, 'error') and resposta.error is not None:
            print(f"❌ Erro no Registo Supabase: {resposta.error.message}")
            return None
            
        print(f"✅ Sucesso: Utilizador {email} cadastrado com segurança na Supabase!")
        return resposta
    except Exception as e:
        print(f"❌ Erro Crítico no Registo: {e}")
        return None

# 4. FUNÇÃO 2: Fazer Login e gerar o Token de Acesso Seguro
def fazer_login_utilizador(email: str, password: str):
    try:
        sessao = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        # Proteção contra falhas silenciosas de senha inválida
        if hasattr(sessao, 'error') and sessao.error is not None:
            print(f"❌ Erro de Credenciais: {sessao.error.message}")
            return None
            
        print(f"🔑 Sucesso: Login efetuado! Token de segurança gerado para {email}.")
        return sessao
    except Exception as e:
        print(f"❌ Erro Crítico no Login: {e}")
        return None

# 5. FUNÇÃO 3: Gerar link de login rápido com o Google
def obter_link_login_google():
    try:
        dados = supabase.auth.get_oauth_nav_url({
            "provider": "google",
            "redirect_to": REDIRECT_URL
        })
        print("🌐 Link de autenticação do Google gerado com sucesso!")
        return dados
    except Exception as e:
        print(f"❌ Erro ao gerar link do Google: {e}")
        return None

# 6. FUNÇÃO 4: Gerar link de login rápido com a Shopify
def obter_link_login_shopify(loja_url: str):
    try:
        dados = supabase.auth.get_oauth_nav_url({
            "provider": "shopify",
            "redirect_to": REDIRECT_URL,
            "options": {
                "scopes": "read_orders,read_fulfillments",
                "provider_options": {"shop": loja_url}
            }
        })
        print(f"🛍️ Link de conexão para a loja Shopify {loja_url} gerado!")
        return dados
    except Exception as e:
        print(f"❌ Erro ao conectar com a Shopify: {e}")
        return None
