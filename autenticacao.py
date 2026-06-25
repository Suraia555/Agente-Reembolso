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

# 3. FUNÇÃO 1: Registar um novo utilizador na nuvem com metadados profissionais
def criar_novo_utilizador(email: str, password: str, nome: str):  # <-- Adicionado o parâmetro 'nome' aqui
    try:
        # O comando .auth.sign_up cria o utilizador e injeta o nome nos metadados seguros (user_metadata)
        resposta = supabase.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "data": {
                    "full_name": nome  # <-- O nome fica guardado na nuvem sob a chave padrão do Supabase
                }
            }
        })
        # Verifica se a nuvem retornou algum erro interno antes de confirmar
        if hasattr(resposta, 'error') and resposta.error is not None:
            print(f"❌ Erro no Registo Supabase: {resposta.error.message}")
            return None
            
        print(f"✅ Sucesso: Utilizador {nome} ({email}) cadastrado com segurança na Supabase!")
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
# =====================================================================
# 🛡️ EXPANSÃO DE IDENTIDADE ENTERPRISE (ETAPAS 1, 2 E 3)
# =====================================================================

# --- ETAPA 1: FLUXO DE REDEFINIÇÃO DE SENHA ESQUECIDA ---

def solicitar_recuperacao_senha(email: str):
    """
    Dispara um e-mail oficial com link criptografado temporário 
    para o utilizador resetar a credencial.
    """
    try:
        resposta = supabase.auth.reset_password_for_email(
            email=email,
            options={"redirect_to": REDIRECT_URL}
        )
        print(f"📧 E-mail de redefinição de senha disparado com sucesso para: {email}")
        return resposta
    except Exception as e:
        print(f"❌ Erro ao solicitar recuperação de senha: {e}")
        return None

def confirmar_nova_senha(nova_password: str):
    """
    Atualiza a senha do utilizador atual na nuvem após ele 
    ter sido autenticado temporariamente pelo link do e-mail.
    """
    try:
        # O Supabase Auth exige que o utilizador já esteja na sessão temporária do link
        resposta = supabase.auth.update_user({
            "password": nova_password
        })
        print("🔒 Sucesso: Nova senha criptografada e salva na nuvem corporativa!")
        return resposta
    except Exception as e:
        print(f"❌ Erro crítico ao confirmar nova senha: {e}")
        return None


# --- ETAPA 2: AUTENTICAÇÃO PASSWORDLESS (MAGIC LINKS & OTP) ---

def enviar_otp_login_rapido(email: str):
    """
    Envia um token numérico de 6 dígitos de uso único (OTP) 
    para o e-mail do cliente, eliminando a necessidade de senhas.
    """
    try:
        resposta = supabase.auth.sign_in_with_otp({
            "email": email,
            "options": {
                "should_create_user": False, # Impede cadastros novos por esta via de segurança
                "redirect_to": REDIRECT_URL
            }
        })
        print(f"🔢 Token OTP de 6 dígitos enviado para o e-mail: {email}")
        return resposta
    except Exception as e:
        print(f"❌ Erro ao disparar e-mail OTP: {e}")
        return None

def verificar_otp_login_rapido(email: str, token_6_digitos: str):
    """
    Valida o token numérico digitado no painel e gera 
    o Token de Acesso JWT oficial caso o código esteja correto.
    """
    try:
        sessao = supabase.auth.verify_otp({
            "email": email,
            "token": token_6_digitos,
            "type": "magiclink" # Define o escopo rigoroso de validação OTP
        })
        print(f"🔑 Sucesso Passwordless: Sessão iniciada via OTP para {email}!")
        return sessao
    except Exception as e:
        print(f"❌ Erro de Validação OTP: Token inválido ou expirado. {e}")
        return None


# --- ETAPA 3: FLUXO DESCENTRALIZADO DE RECUPERAÇÃO DE E-MAIL ---

def recuperar_email_via_loja_shopify(dominio_loja_shopify: str):
    """
    Mecanismo de Elite: Localiza o e-mail do utilizador na gringa 
    apenas utilizando a credencial da loja cadastrada no banco de dados.
    """
    try:
        # A. Busca na tabela de encomendas qual o UUID que é dono dessa loja
        resposta_db = supabase.table("encomendas").select("user_id")\
            .eq("transportadora", dominio_loja_shopify).execute() # Usando o campo de vínculo da loja
            
        if not resposta_db.data:
            print("❌ Nenhuma credencial de loja localizada para este domínio.")
            return None
            
        # Captura o UUID do proprietário real
        uuid_dono = resposta_db.data[0].get("user_id")
        
        # B. Nota de Engenharia: Como o auth.users é protegido por cibersegurança, 
        # em produção este passo consulta a sua tabela espelho pública de perfis (profiles)
        resposta_perfil = supabase.table("perfis").select("email").eq("id", uuid_dono).execute()
        
        if resposta_perfil.data:
            email_recuperado = resposta_perfil.data[0].get("email")
            print(f"🔍 Identidade Localizada de forma descentralizada! Dono: {email_recuperado}")
            return email_recuperado
            
        return None
    except Exception as e:
        print(f"❌ Erro no fluxo descentralizado de recuperação: {e}")
        return None
