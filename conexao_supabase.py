import os
import random
from dotenv import load_dotenv
from supabase import create_client, Client

# 1. Carrega as chaves secretas do .env
load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")

# 🚨 DEFINIÇÃO DE SEGURANÇA: UUID do teu utilizador piloto de testes
# Podes capturar este ID diretamente no painel de Autenticação do teu Supabase
UUID_UTILIZADOR_TESTE = "INSIRA_AQUI_O_UUID_DO_TEU_UTILIZADOR_DE_TESTES"

print("--- 🏋️ INICIANDO TESTE DE CARGA LOCAL SEGURO: 500 ENCOMENDAS ---")

try:
    # 2. Conecta à Supabase
    supabase: Client = create_client(url, key)
    
    # 3. Gerador Automático de 500 Encomendas na Memória RAM
    lista_carga = []
    transportadoras_teste = ["Correios", "Jadlog", "Loggi", "Total Express"]
    
    for i in range(1, 501):
        numero_aleatorio = random.randint(100000, 999999)
        encomenda = {
            "user_id": UUID_UTILIZADOR_TESTE,  # 🛡️ Escudo ativo: Cada pacote pertence estritamente ao utilizador de teste
            "codigo_rastreio": f"BR{numero_aleatorio}TESTE",
            "transportadora": random.choice(transportadoras_teste),
            "status": "ELEGÍVEL PARA REEMBOLSO (TESTE DE CARGA)"
        }
        lista_carga.append(encomenda)
        
    print(f"📦 Sucesso: 500 encomendas estruturadas com UUID de segurança. Disparando em lote...")
    
    # 4. Envio em Massa (Bulk Insert) protegido com try/except
    dados = supabase.table("encomendas").insert(lista_carga).execute()
    
    print("🔥 VITÓRIA! 500 encomendas gravadas na Supabase em simultâneo sob isolamento estrito!")
    
except Exception as e:
    print(f"❌ Erro Crítico durante o teste de carga: {e}")
