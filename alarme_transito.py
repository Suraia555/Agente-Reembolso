import os
from datetime import datetime, timedelta

print("--- MÓDULO ADVANCED: PRE-EMPTIVE FAILURE DETECTION ENGINE ATIVO ---")

def avaliar_risco_atraso_em_transito(data_envio_iso: str, data_ultimo_checkpoint_iso: str, status_atual_hub: str, prazo_garantido_horas: int = 48) -> dict:
    """
    Pré-Detetor de Falhas Logísticas.
    Calcula a janela de tempo decorrido desde o envio e avalia se o checkpoint
    atual do pacote justifica a ativação do Alarme Preventivo de Quebra.
    """
    try:
        # 1. Converte as strings ISO da Shopify/Transportadora para objetos datetime reais
        data_envio = datetime.fromisoformat(data_envio_iso.replace("Z", "+00:00"))
        data_checkpoint = datetime.fromisoformat(data_ultimo_checkpoint_iso.replace("Z", "+00:00"))
        
        data_atual = datetime.now(data_envio.tzinfo)
        
        # 2. CALCULADORA DE LATÊNCIA TEMPORAL (RAM COMPUTATION)
        horas_desde_envio = round((data_atual - data_envio).total_seconds() / 3600, 1)
        horas_parado_no_hub = round((data_atual - data_checkpoint).total_seconds() / 3600, 1)
        
        # 3. ALGORITMO PREDITIVO DE QUEBRA DE SLA
        limite_critico_horas = prazo_garantido_horas * 0.75
        
        # 🛡️ Blindagem Ortográfica: Todas as variáveis unificadas sem o 'c'
        ativar_alarme_preventivo = False
        probabilidade_falha = 15.0 
        mensagem_alarme = "✅ Rota dentro dos parâmetros de velocidade estimados."
        
        status_hostis_hub = ["sorting", "held", "arrived at origin facility", "hub processing"]
        
        if horas_desde_envio >= limite_critico_horas and status_atual_hub.lower() in status_hostis_hub:
            ativar_alarme_preventivo = True
            probabilidade_falha = min(92.0, round(75.0 + (horas_parado_no_hub * 0.5), 1))
            mensagem_alarme = (
                f"🚨 ALERTA PREVENTIVO: Detetámos que o pacote tem {probabilidade_falha}% de probabilidade de quebrar o prazo. "
                f"O CarrierRefund já preparou a minuta jurídica e vai disparar o reembolso automaticamente."
            )
            
        return {
            "sucesso": True,
            "horas_em_transito": horas_desde_envio,
            "horas_congelado_no_hub": horas_parado_no_hub,
            "alarme_preventivo_ativo": ativar_alarme_preventivo, # 🚨 Corrigido aqui também!
            "probabilidade_quebra_prazo_porcento": probabilidade_falha,
            "insight_retencao_lojava": mensagem_alarme
        }
        
    except Exception as e:
        print(f"❌ Erro crítico no motor preditivo de pré-notificação: {e}")
        return {
            "sucesso": False,
            "alarme_preventivo_ativo": False,
            "probabilidade_quebra_prazo_porcento": 0.0,
            "insight_retencao_lojava": "Erro interno ao processar telemetria de trânsito."
        }

