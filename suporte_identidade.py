import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

# Inicializa o cliente seguro para o módulo de suporte
supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

print("--- MÓDULO DE SUPORTE: RECUPERAÇÃO DESCENTRALIZADA ATIVO ---")

def recuperar_email_via_loja_shopify(dominio_loja_shopify: str) -> str:
    """
    Mecanismo de Elite: Localiza o e-mail do utilizador na nuvem
    utilizando o subdomínio da loja Shopify registado nas encomendas.
    """
    try:
        # A. Limpa a entrada do utilizador removendo espaços em branco
        loja_limpa = dominio_loja_shopify.strip()
        
        # B. Busca reversa na tabela encomendas caçando o user_id dono da loja
        resposta_db = supabase.table("encomendas")\
            .select("user_id")\
            .eq("transportadora", loja_limpa)\
            .execute()
            
        if not resposta_db.data:
            print(f"🔍 Suporte: Nenhuma credencial de loja localizada para '{loja_limpa}'.")
            return "LOJA_NAO_ENCONTRADA"
            
        # Captura o primeiro UUID que aparecer vinculado a essa loja de e-commerce
        encomenda_encontrada = resposta_db.data[0]
        uuid_dono = encomenda_encontrada.get("user_id")
        
        # C. Consulta a tabela espelho pública 'perfis' para extrair o e-mail criptografado/seguro
        # Nota: Usamos a service_role do Supabase ou uma view segura se o RLS bloquear
        resposta_perfil = supabase.table("perfis")\
            .select("email")\
            .eq("id", uuid_dono)\
            .execute()
            
        r_data = resposta_perfil.data
        if not r_data:
            print("🚨 Alerta: UUID localizado, mas perfil espelho não encontrado.")
            return "PERFIL_INCOMPLETO"
       
        email_real = r_data[0].get("email")
        print(f"✅ Identidade Localizada com Sucesso! Dono: {email_real}")
        return email_real
        
    except Exception as e:
        print(f"❌ Erro crítico no fluxo descentralizado de recuperação: {e}")
        return f"ERROR_INTERNAL: {str(e)}"

def mascarar_email_privacidade(email: str) -> str:
    """
    Mascarador de segurança para evitar vazamento de dados na interface.
    Transforma 'engenheira@carrierrefund.com' em 'e*********a@carrierrefund.com'.
    """
    try:
        if "@" not in email:
            return email
            
        usuario, dominio = email.split("@", 1)
        if len(usuario) <= 2:
            return f"{usuario[0]}*@{dominio}"
            
        return f"{usuario[0]}{'*' * (len(usuario) - 2)}{usuario[-1]}@{dominio}"
    except Exception:
        return "email_protegido@carrierrefund.com"
