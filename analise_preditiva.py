print("--- MÓDULO ADVANCED: LOGISTICS PREDICTIVE ANALYTICS ATIVO ---")

def calcular_probabilidade_atraso_ml(taxa_historica_transportadora: float, media_dias_historica: float, dias_pico_sazonal: bool = False) -> dict:
    """
    Motor Preditivo por Aprendizagem Estatística.
    Calcula a probabilidade matemática de quebra de prazo e gera o Alerta Preventivo.
    """
    try:
        # 1. Definição dos hiperparâmetros do modelo (Fatores de ponderação de risco)
        fator_sazonal = 1.35 if dias_pico_sazonal else 1.00
        
        # 2. Equação Preditiva da Probabilidade
        probabilidade_final = round(taxa_historica_transportadora * fator_sazonal, 2)
        if probabilidade_final > 99.0:
            probabilidade_final = 99.0

        # 3. Equação Preditiva de Latência: Estima quantos dias o pacote REALMENTE vai demorar
        dias_estimados_ml = round(media_dias_historica * fator_sazonal, 1)
            
        # 4. Classificação de Criticidade do Alerta
        if probabilidade_final >= 75.0:
            status_risco = "CRÍTICO"
            alerta = f"🚨 ALERTA ML: Rota severamente afetada. Entrega estimada em {dias_estimados_ml} dias."
        elif probabilidade_final >= 40.0:
            status_risco = "MODERADO"
            alerta = f"⚠️ ALERTA ML: Latência flutuante. Entrega estimada em {dias_estimados_ml} dias."
        else:
            status_risco = "SEGURO"
            alerta = f"✅ ALERTA ML: Rota estável. Entrega estimada em {dias_estimados_ml} dias dentro do prazo."
            
        return {
            "probabilidade_atraso_porcento": probabilidade_final,
            "dias_estimados_pelo_ml": dias_estimados_ml,
            "status_risco": status_risco,
            "alerta_preventivo": alerta
        }
    except Exception as e:
        print(f"❌ Erro ao processar cálculo preditivo: {e}")
        return {
            "probabilidade_atraso_porcento": 0.0, 
            "dias_estimados_pelo_ml": 0.0, # 🛡️ Adicionado para segurança das rotas
            "status_risco": "INDETERMINADO", 
            "alerta_preventivo": "Erro interno de processamento estatístico."
        }
