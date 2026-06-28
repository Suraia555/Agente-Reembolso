print("--- MÓDULO ENTERPRISE: GAMIFICAÇÃO E RETENÇÃO ATIVO ---")

def calcular_nivel_tubarao(total_ganhas: int) -> dict:
    """
    Motor de Gamificação do CarrierRefund.
    Determina o badge e os privilégios do lojista baseado no volume de sucesso.
    """
    if total_ganhas >= 100:
        return {
            "badge": "Grande Tubarão do E-commerce",
            "nivel": 3,
            "prioridade_ia": "CRÍTICA_THREADS_EXCLUSIVAS"
        }
    elif total_ganhas >= 20:
        return {
            "badge": "Delfim da Logística",
            "nivel": 2,
            "prioridade_ia": "ALTA_FILA_ACELERADA"
        }
    else:
        return {
            "badge": "Peixe-Piloto Autodidata",
            "nivel": 1,
            "prioridade_ia": "PADRÃO"
        }

def formatar_evento_live_ticker(id_encomenda: str, transportadora: str) -> dict:
    """
    Prepara os metadados mascarados para o Live Refund Ticker global.
    Mantém o anonimato absoluto do lojista enquanto exibe a prova social.
    """
    id_limpo = id_encomenda.strip()
    
    # Mascara o ID para privacidade (Ex: ENC-9412 vira EN**12)
    if len(id_limpo) > 4:
        id_mascarado = f"{id_limpo[:2]}**{id_limpo[-2:]}"
    else:
        id_mascarado = "Pedido_Protegido"
        
    return {
        "mensagem_ticker": f"⚡ Vitória Logística: {id_mascarado} em contestação via {transportadora}!",
        "sucesso": True
    }
