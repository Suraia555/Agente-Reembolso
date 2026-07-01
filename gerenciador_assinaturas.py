import os
from dotenv import load_dotenv
from supabase import create_client, Client

# 1. Inicialização blindada de credenciais da nuvem
load_dotenv()
supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

print("--- 💳 MÓDULO ENTERPRISE: GERENCIADOR DE ASSINATURAS ATIVO ---")

def processar_limites_e_regras_faturamento(plano_nome: str) -> dict:
    """
    Matriz de Engenharia Financeira (Estilo OpenAI/Claude Enterprise).
    Define dinamicamente os limites de pacotes, a taxa de comissão de sucesso 
    e os módulos de elite libertados com base no plano contratado.
    """
    plano_limpo = plano_nome.strip().lower()
    
    # 🎯 CONFIGURAÇÃO DAS REGRAS DE NEGÓCIO DA STARTUP
    if "enterprise" in plano_limpo or "120" in plano_limpo:
        return {
            "plano_oficial": "ENTERPRISE",
            "limite_encomendas_mes": 999999, # Praticamente ilimitado para grandes operações
            "taxa_sucesso_fee_porcento": 10.0, # Margem agressiva de 10%
            "modulo_preditivo_ml_ativo": True,
            "modulo_ledger_blockchain_ativo": True
        }
    elif "pro" in plano_limpo or "50" in plano_limpo:
        return {
            "plano_oficial": "PRO",
            "limite_encomendas_mes": 5000, # Escalável para e-commerces médios
            "taxa_sucesso_fee_porcento": 15.0, # Margem intermediária de 15%
            "modulo_preditivo_ml_ativo": True,
            "modulo_ledger_blockchain_ativo": False # Exclusivo do Enterprise!
        }
    else:
        # Fallback de segurança: Plano Starter padrão ($20/mês)
        return {
            "plano_oficial": "STARTER",
            "limite_encomendas_mes": 200, # Limite estrito de 200 pacotes/mês
            "taxa_sucesso_fee_porcento": 20.0, # Taxa base de 20%
            "modulo_preditivo_ml_ativo": False,
            "modulo_ledger_blockchain_ativo": False
        }

def sincronizar_assinatura_e_bloqueios(uuid_cliente: str, lemon_sub_id: str, variant_name: str, status_lemon: str) -> bool:
    """
    Core Engine de Faturamento.
    Sincroniza o estado do plano e injeta as travas e privilégios contratuais na nuvem.
    Se o cliente ficar inativo por cancelamento ou chargeback, bloqueia os acessos imediatamente.
    """
    try:
        # Padrão internacional de segurança: 'active' ou 'on_trial' (período de testes) liberta o SaaS
        status_final_saas = "ATIVO" if status_lemon in ["active", "on_trial"] else "INATIVO"
        
        # 1. Extrai as regras de faturamento baseadas no plano comprado
        regras = processar_limites_e_regras_faturamento(variant_name)
        
        # 2. Executa o Upsert na tabela faturamento_assinaturas da Supabase
        resposta = supabase.table("faturamento_assinaturas").upsert({
            "user_id": uuid_cliente,
            "lemon_subscription_id": str(lemon_sub_id),
            "plano_nome": regras["plano_oficial"],
            "status_assinatura": status_final_saas,
            # Injetamos as métricas sofisticadas diretamente na tabela para o teu main.py ler
            "limite_mensal_pacotes": regras["limite_encomendas_mes"],
            "comissao_success_fee": regras["taxa_sucesso_fee_porcento"],
            "acesso_motor_preditivo": regras["modulo_preditivo_ml_ativo"],
            "acesso_ledger_blockchain": regras["modulo_ledger_blockchain_ativo"]
        }).execute()
        
        # 🛡️ PROTEÇÃO DE CAIXA REVERSA PARA AFILIADOS (A tua regra de negócio)
        if status_final_saas == "INATIVO":
            # Se o lojista ficou inadimplente ou cancelou, removemos o direito de saque do afiliado
            supabase.table("parcerias_afiliados").update({
                "status_premio": "AGUARDANDO_VALIDACAO"
            }).eq("indicado_id", uuid_cliente).execute()
            print(f"📉 Assinaturas: Contrato quebrado por [{uuid_cliente[:8]}]. Prémio do afiliado revertido para quarentena.")
            
        if resposta.data:
            print(f"💳 Assinaturas: Cliente [{uuid_cliente[:8]}] sincronizado no plano {regras['plano_oficial']} ({status_final_saas}).")
            return status_final_saas == "ATIVO"
            
        return False
    except Exception as e:
        print(f"❌ Erro crítico no processador do gerenciador de assinaturas: {e}")
        return False
