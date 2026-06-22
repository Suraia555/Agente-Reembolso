import os
from dotenv import load_dotenv
from supabase import create_client, Client

# 1. Carrega as credenciais de segurança do arquivo oculto .env
load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")

# 2. Inicializa o cliente seguro da Supabase
supabase: Client = create_client(url, key)

print("--- REQUISITO DE SEGURANÇA: MÓDULO SUPABASE AUTH ---")

# 3. FUNÇÃO 1: Registar um novo utilizador na nuvem
def criar_novo_utilizador(email: str, password: str):
    try:
        # O comando .auth.sign_up cria o utilizador e encripta a password automaticamente na gringa
        resposta = supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        print(f"✅ Sucesso: Utilizador {email} cadastrado com segurança na Supabase!")
        return resposta
    except Exception as e:
        print(f"❌ Erro no Registo: {e}")
        return None

# 4. FUNÇÃO 2: Fazer Login e gerar o Token de Acesso Seguro
def fazer_login_utilizador(email: str, password: str):
    try:
        # O .auth.sign_in_with_password valida as credenciais e inicia a sessão
        sessao = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        print(f"🔑 Sucesso: Login efetuado! Token de segurança gerado para {email}.")
        return sessao
    except Exception as e:
        print(f"❌ Erro no Login: Credenciais inválidas. {e}")
        return None
# Teste prático: Criando o primeiro cliente piloto na nuvem
criar_novo_utilizador("cliente_teste@carrierrefund.com", "SenhaSegura123!")
