print("--- MÓDULO ADVANCED: LOGISTICS PREDICTIVE ANALYTICS ATIVO ---")

def calcular_probabilidade_atraso_ml(taxa_historica_transportadora: float, dias_pico_sazonal: bool = False) -> dict:
    """
    Motor Preditivo por Aprendizagem Estatística.
    Calcula a probabilidade matemática de quebra de prazo e gera o Alerta Preventivo.
    """
    try:
        # Fator de ponderação estatística básico (Machine Learning Layer Simulado em RAM)
        fator_risco = 1.2 if dias_pico_sazonal else 1.0
        probabilidade_final = round(taxa_historica_transportadora * fator_risco, 2)
        
        # Garante o teto estatístico de 99%
        if probabilidade_final > 99.0:
            probabilidade_final = 99.0
            
        # Determina o nível de criticidade e monta o Alerta Preventivo
        if probabilidade_final >= 75.0:
            status_risco = "CRÍTICO"
            alerta = "🚨 ALERTA PREVENTIVO: Rota com altíssimo índice de quebra. Considere despachar via concorrente."
        elif probabilidade_final >= 40.0:
            status_risco = "MODERADO"
            alerta = "⚠️ ALERTA PREVENTIVO: Latência acima da média detectada nesta transportadora."
        else:
            status_risco = "SEGURO"
            alerta = "✅ Rota estável com alto índice de entrega no prazo garantido."
            
        return {
            "probabilidade_atraso_porcento": probabilidade_final,
            "status_risco": status_risco,
            "alerta_preventivo": alerta
        }
    except Exception as e:
        print(f"❌ Erro ao processar cálculo preditivo: {e}")
        return {"probabilidade_atraso_porcento": 0.0, "status_risco": "INDETERMINADO", "alerta_preventivo": "Erro interno de processamento estatístico."}
