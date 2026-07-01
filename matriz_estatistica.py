import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

# Inicializa o cliente seguro para o módulo estatístico
supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

print("--- MÓDULO ADVANCED: DISPUTE WIN-RATE MATRIX ATIVO ---")

def determinar_estrategia_agressividade_hub(centro_triagem: str) -> dict:
    """
    Analisa a matriz estatística de vitórias do centro de triagem na Supabase.
    Determina dinamicamente o nível de agressividade e injeta o tom jurídico ideal [ENC-503].
    """
    try:
        # 1. Consulta a View estatística na nuvem filtrando pelo Hub ID
        resposta_db = supabase.table("view_matriz_win_rate")\
            .select("taxa_sucesso_porcento")\
            .eq("centro_triagem_id", centro_triagem.strip()).execute()
            
        taxa_sucesso = 100.0 # Se o Hub for novo, assumimos 100% de confiança inicial
        
        # O teu escudo antibloqueio de SDK do Supabase
        if resposta_db.data and isinstance(resposta_db.data, list) and len(resposta_db.data) > 0:
            taxa_sucesso = float(resposta_db.data[0].get("taxa_sucesso_porcento", 100.0))
            
        # 2. ALGORITMO DE SELECÇÃO DE TOM JURÍDICO (Game Theory Strategy)
        # Se a taxa de sucesso for inferior a 45%, o Hub é considerado hostil e rejeita por defeito.
        if taxa_sucesso < 45.0:
            tom_juridico = "MAXIMUM_AGGRESSION"
            instrucao_prompt = (
                "The target logistics hub has a history of bad-faith claim rejections. "
                "Write with maximum legal aggression. Cite federal transport regulations and demand immediate escalation."
            )
        elif taxa_sucesso < 75.0:
            tom_juridico = "FIRM_CORPORATE"
            instrucao_prompt = (
                "The target logistics hub is moderately compliant. "
                "Use a firm, corporate-legal tone, emphasizing contract terms clearly."
            )
        else:
            tom_juridico = "STANDARD_FORMAL"
            instrucao_prompt = "Standard formal claim. State the delay facts clearly and requesting the contractual credit."
            
        return {
            "sucesso": True,
            "centro_analisado": centro_triagem,
            "win_rate_historico_porcento": taxa_sucesso,
            "nivel_agressividade": tom_juridico,
            "prompt_mutation_english": instrucao_prompt # Prompt mantido estritamente em inglês corporativo [ENC-503]
        }
        
    except Exception as e:
        print(f"❌ Erro ao processar matriz estatística de win-rate: {e}")
        return {
            "sucesso": False,
            "centro_analisado": centro_triagem,
            "win_rate_historico_porcento": 50.0,
            "nivel_agressividade": "STANDARD_FORMAL",
            "prompt_mutation_english": "Standard formal claim."
        }
