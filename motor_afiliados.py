import os
from datetime import datetime, timezone
from dotenv import load_dotenv
from supabase import create_client, Client

# 1. Inicialização blindada de credenciais da nuvem
load_dotenv()
supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

print("--- 👥 MÓDULO ENTERPRISE: MOTOR DE AFILIADOS CPA ATIVO ---")

def registrar_vinculo_afiliado_inicial(uuid_afiliado: str, uuid_indicado: str) -> dict:
    """
    Regista o gancho inicial de convite na tabela parcerias_afiliados.
    O prémio nasce bloqueado no estado padrão 'AGUARDANDO_VALIDACAO'.
    """
    try:
        # Impede auto-indicação (Segurança de Caixa)
        if uuid_afiliado == uuid_indicado:
            return {"sucesso": False, "erro": "Operação bloqueada: Auto-indicação detetada."}
            
        resposta = supabase.table("parcerias_afiliados").insert({
            "afiliado_id": uuid_afiliado,
            "indicado_id": uuid_indicado,
            "status_premio": "AGUARDANDO_VALIDACAO",
            "valor_usd": 5.00
        }).execute()
        
        if resposta.data:
            print(f"👥 Growth: Novo vínculo registado. Utilizador [{uuid_indicado[:8]}] indicado por [{uuid_afiliado[:8]}].")
            return {"sucesso": True, "dados": resposta.data[0]}
            
        return {"sucesso": False, "erro": "Falha na persistência do vínculo aduaneiro."}
    except Exception as e:
        print(f"❌ Erro ao registar vínculo de afiliado: {e}")
        return {"sucesso": False, "erro": str(e)}


def validar_e_disparar_cronometro_cpa(uuid_indicado: str) -> dict:
    """
    🛡️ BARREIRA ANTIFRAUDE CORE: Executa a validação mecânica de idoneidade.
    Verifica se o lojista gringo indicado pagou e já subiu pelo menos 1 pacote real.
    Se estiver limpo, ativa o estado 'PRONTO_PARA_SAQUE' e carimba a data UTC, 
    iniciando oficialmente a contagem regressiva da tua retenção de 15 dias.
    """
    try:
        # A. Localiza a parceria pendente do utilizador indicado
        parceria_db = supabase.table("parcerias_afiliados").select("*")\
            .eq("indicado_id", uuid_indicado)\
            .eq("status_premio", "AGUARDANDO_VALIDACAO").execute()
            
        if not parceria_db.data or len(parceria_db.data) == 0:
            return {"sucesso": False, "motivo": "Nenhuma comissão CPA pendente localizada para este UUID."}
            
        registro_parceria = parceria_db.data[0]
        id_parceria = registro_parceria.get("id")
        
        # B. 🚨 EXIGÊNCIA INDUSTRIAL: Verifica se a conta já possui volume de pacotes inserido
        verificacao_pacotes = supabase.table("encomendas").select("codigo_rastreio")\
            .eq("user_id", uuid_indicado).limit(1).execute()
            
        if not verificacao_pacotes.data or len(verificacao_pacotes.data) == 0:
            print(f"⚠️ Antifraude: Usuário [{uuid_indicado[:8]}] ativou o plano, mas a conta está vazia. Saldo retido.")
            return {"sucesso": False, "motivo": "Conta sem histórico de encomendas ativas na Shopify/CSV."}
            
        # C. LIBERAÇÃO CRONOMETRADA: Grava o timestamp exato em UTC na nuvem do Supabase
        timestamp_atual_utc = datetime.now(timezone.utc).isoformat()
        
        resposta_update = supabase.table("parcerias_afiliados").update({
            "status_premio": "PRONTO_PARA_SAQUE",
            "data_validacao_premio": timestamp_atual_utc
        }).eq("id", id_parceria).execute()
        
        if resposta_update.data:
            print(f"💰 Payout Guard: Prémio validado para a parceria [{id_parceria[:8]}]. Janela de 15 dias aberta.")
            return {"sucesso": True, "dados": resposta_update.data[0]}
            
        return {"sucesso": False, "erro": "Falha ao gravar metadados de validação."}
    except Exception as e:
        print(f"❌ Erro crítico no motor de validação CPA: {e}")
        return {"sucesso": False, "erro": str(e)}
