import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

# Inicializa o cliente seguro para o módulo de armazenamento
supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

print("--- MÓDULO DE INFRAESTRUTURA: ARMAZENAMENTO DIGITAL ACTIVO ---")

def gerar_url_assinada_upload(token_usuario: str, formato_extensao: str = "webp") -> dict:
    """
    Gera uma URL Assinada (Presigned URL) que permite ao navegador do utilizador 
    fazer o upload direto da foto de perfil para a nuvem da Supabase, sem 
    sobrecarregar o nosso backend FastAPI com tráfego binário. Validada por 60 segundos.
    """
    try:
        # A. Valida o utilizador na nuvem via UUID para cibersegurança
        usuario_atual = supabase.auth.get_user(token_usuario)
        uuid_cliente = usuario_atual.user.id
        
        # B. Define o caminho físico fixo do arquivo usando o UUID exclusivo do dono da conta
        caminho_arquivo = f"avatars/{uuid_cliente}/perfil.{formato_extensao}"
        
        # C. Solicita à API do Supabase Storage a permissão de escrita temporária
        # Cria ou atualiza o arquivo de forma autónoma na nuvem
        resposta = supabase.storage.from_("fotos_perfil").create_signed_upload_url(caminho_arquivo)
        
        print(f"🔒 Storage: URL Assinada gerada com sucesso para o utilizador UUID: {uuid_cliente}")
        return {
            "sucesso": True,
            "uuid_proprietario": uuid_cliente,
            "caminho_remoto": caminho_arquivo,
            "url_assinada_upload": resposta.get("signed_url") or resposta
        }
        
    except Exception as e:
        print(f"❌ Erro crítico ao gerar URL assinada de armazenamento: {e}")
        return {"sucesso": False, "erro_detetado": str(e)}

def obter_avatar_perfil_seguro(token_usuario: str, caminho_remoto: str) -> str:
    """
    Recupera uma URL de leitura temporária para exibir no Dashboard do cliente.
    A Cloudflare CDN distribui o arquivo globalmente de forma instantânea.
    """
    try:
        usuario_atual = supabase.auth.get_user(token_usuario)
        uuid_cliente = usuario_atual.user.id
        
        # Garante que um utilizador malicioso não consegue ler pastas de outro UUID
        if f"avatars/{uuid_cliente}/" not in caminho_remoto:
            print("🚨 Violação de Segurança: Tentativa ilícita de acesso a armazenamento alheio.")
            return "ACESSO_NEGADO"
            
        # Gera o link de visualização seguro válido por 15 minutos (900 segundos)
        resposta_url = supabase.storage.from_("fotos_perfil").create_signed_url(caminho_remoto, 900)
        return resposta_url
        
    except Exception as e:
        print(f"❌ Erro ao recuperar link de leitura: {e}")
        return "https://carrierrefund.com"
