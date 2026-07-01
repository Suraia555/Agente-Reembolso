import os
from datetime import datetime

print("--- MÓDULO ADVANCED: CROSS-BORDER DUTY SCRAPER ATIVO ---")

def calcular_latencia_operacional_pura(logs_rastreio: list, dias_totais_transito: int, prazo_garantido: int) -> dict:
    """
    Isolador Alfandegário Autónomo.
    Varre os logs de rastreio, extrai os carimbos de data/hora de entrada e saída 
    da alfândega e calcula o tempo líquido de responsabilidade da transportadora.
    """
    try:
        timestamp_entrada = None
        timestamp_saida = None
        
        # 🕵️ PALAVRAS-CHAVE DA GRINGA: Termos padrão utilizados por FedEx/DHL para alfândega
        termos_entrada = ["held in customs", "customs clearance", "regulatory review", "border control"]
        termos_saida = ["customs cleared", "released by customs", "international shipment release"]
        
        # 1. Varre a lista de logs procurando os carimbos de tempo aduaneiros
        for evento in logs_rastreio:
            texto_log = evento.get("descricao", "").strip().lower()
            data_str = evento.get("timestamp", "") # Formato esperado: "2026-03-25T14:00:00"
            
            if not data_str:
                continue
                
            # Identifica a entrada na alfândega
            if any(termo in texto_log for termo in termos_entrada) and not timestamp_entrada:
                timestamp_entrada = datetime.fromisoformat(data_str)
                
            # Identifica a saída/libertação da alfândega
            if any(termo in texto_log for termo in termos_saida) and not timestamp_saida:
                timestamp_saida = datetime.fromisoformat(data_str)

        # 2. ALGORITMO MATEMÁTICO DE SUBTRAÇÃO DE RETENÇÃO
        dias_retidos_alfandega = 0.0
        
        if timestamp_entrada and timestamp_saida:
            # Calcula a diferença exata em segundos e converte para fração de dias
            diferenca_tempo = timestamp_saida - timestamp_entrada
            dias_retidos_alfandega = round(diferenca_tempo.total_seconds() / 86400, 1)

        # Calcula quantos dias a transportadora gastou por conta própria
        dias_operacionais_puros = round(dias_totais_transito - dias_retidos_alfandega, 1)
        
        # Se os dias operacionais puros forem maiores do que o prazo estipulado em contrato, cabe estorno!
        elegivel_pos_alfandega = dias_operacionais_puros > prazo_garantido
        
        return {
            "sucesso": True,
            "dias_totais_transito": dias_totais_transito,
            "dias_retidos_na_alfandega": dias_retidos_alfandega,
            "dias_operacionais_puros_transportadora": dias_operacionais_puros,
            "elegivel_para_reembolso": elegivel_pos_alfandega,
            "motivo_calculo": f"Retenção de {dias_retidos_alfandega} dias removida do cálculo de culpa."
        }
        
    except Exception as e:
        print(f"❌ Erro crítico no isolador alfandegário: {e}")
        return {
            "sucesso": False,
            "dias_totais_transito": dias_totais_transito,
            "dias_retidos_na_alfandega": 0.0,
            "dias_operacionais_puros_transportadora": float(dias_totais_transito),
            "elegivel_para_reembolso": dias_totais_transito > prazo_garantido,
            "erro": str(e)
        }
  
  # Bloco temporário de validação local (Apaga-se após o sucesso)
if __name__ == "__main__":
    # Simulação de um pacote que demorou 8 dias no total (Prazo contratado era de 5 dias)
    # Mas repara: ele ficou retido 3 dias na alfândega de Miami!
    logs_exemplo = [
        {"timestamp": "2026-06-20T08:00:00", "descricao": "Shipment arrived at hub"},
        {"timestamp": "2026-06-21T10:00:00", "descricao": "Held in Customs for regulatory review"}, # Entrada
        {"timestamp": "2026-06-24T10:00:00", "descricao": "International shipment release - Customs cleared"}, # Saída (3 dias depois)
        {"timestamp": "2026-06-28T17:00:00", "descricao": "Delivered to destination"}
    ]
    
    print("🚀 Executando teste de integridade do isolador alfandegário...")
    resultado = calcular_latencia_operacional_pura(
        logs_rastreio=logs_exemplo, 
        dias_totais_transito=8, 
        prazo_garantido=5
    )
    print(f"📊 Resposta do Motor: {resultado}")
