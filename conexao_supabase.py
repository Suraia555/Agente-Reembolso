import os
from dotenv import load_dotenv
from supabase import create_client, Client

# 1. Carrega as variáveis de ambiente protegidas
load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")

print("--- CONECTANDO À NUVEM DA SUPABASE ---")

try:
    # 2. Inicializa o cliente oficial da Supabase
    supabase: Client = create_client(url, key)
    print("✅ Sucesso: O Python estabeleceu ligação com os servidores da Supabase!")
    
except Exception as e:
    print(f"❌ Erro na ligação: {e}")
