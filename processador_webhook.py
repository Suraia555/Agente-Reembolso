import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

# Inicializa o cliente seguro para o módulo autónomo
supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

print("--- MÓDULO AUTÓNOMO: AUTO-DISPUTE WEBHOOK MOTOR ATIVO ---")

async def processar_evento_webhook_shopify(payload_shopify: dict) -> dict:
    """
    Core Engine de Escala Automatizada.
    Processa o payload bruto enviado em tempo real pelos servidores da Shopify,
    calcula as métricas de atraso e persiste os dados sob proteção relacional.
    """
    try:
        # A. Extrai os metadados vitais do pacote enviados pela API da Shopify
        order_id = str(payload_shopify.get("id", ""))
        shipping_lines = payload_shopify.get("shipping_lines", [])
        
        # Procura o código de rastreio (tracking_number) dentro do payload da Shopify
        fulfillments = payload_shopify.get("fulfillments", [])
        codigo_rastreio = ""
        transportadora = "Desconhecida"
        
        if fulfillments:
            tracking_info = fulfillments[0]
            codigo_rastreio = tracking_info.get("tracking_number", "").strip()
            transportadora = tracking_info.get("tracking_company", "Generic").strip()
            
        # B. Escudo de Validação: Se a encomenda não tiver rastreio ativo, ignora o evento de forma limpa
        if not codigo_rastreio:
            return {"sucesso": False, "motivo": "Encomenda sem código de rastreio ativo na Shopify."}
            
        # C. EXTRAÇÃO DA DATA REAL DA SHOPIFY (Substitui os números fixos!)
        from datetime import datetime
        
        # Captura a data em que o gringo comprou (ex: "2026-03-25T14:00:00Z")
        created_at_shopify = payload_shopify.get("created_at", "")
        
        if created_at_shopify:
            # Converte a string da Shopify para um objeto de data real do Python
            # Corta o 'Z' ou fusos horários para simplificar a matemática pura
            data_pedido = datetime.fromisoformat(created_at_shopify.replace("Z", "+00:00"))
            data_atual = datetime.now(data_pedido.tzinfo)
            
            # Calcula em tempo real quantos dias o pacote já está em trânsito na vida real
            dias_decorridos = (data_atual - data_pedido).days
        else:
            dias_decorridos = 0 # Fallback de segurança se a Shopify falhar no timestamp

        # D. INTEGRAÇÃO COM O TEU MOTOR DE ML (Simulação de inputs da View da Supabase)
        # Em produção, o webhook puxa estes 2 dados da tua 'view_latencia_transportadoras'
        taxa_historica_db = 45.0   # Exemplo: 45% de atrasos históricos nesta rota
        media_dias_db = 4.2        # Exemplo: Esta transportadora costuma demorar 4.2 dias
        
        # Invoca o teu motor preditivo passando os dados reais + se estamos em Black Friday/Natal
        insights_ml = calcular_probabilidade_atraso_ml(
            taxa_historica_transportadora=taxa_historica_db,
            media_dias_historica=media_dias_db,
            dias_pico_sazonal=True # Ativa o multiplicador de Machine Learning se for época alta
        )
        
        prazo_previsto_pelo_ml = insights_ml.get("dias_estimados_pelo_ml", 5.0)
        
        # E. MATEMÁTICA PREDITIVA FINAL
        # Se os dias que o pacote já leva na rua ultrapassarem a previsão do ML, dispara o estorno!
        if dias_decorridos > prazo_previsto_pelo_ml:
            status_logistico = "ELEGÍVEL PARA REEMBOLSO"
        else:
            status_logistico = "ENTREGUE_NO_PRAZO"
        
        # Nota de Engenharia: O webhook identifica o user_id procurando a conexão ativa
        # através do domínio da loja associado ou metadados de instalação
        
        resultado_processamento = {
            "shopify_order_id": order_id,
            "codigo_rastreio": codigo_rastreio,
            "transportadora": transportadora,
            "prazo_prometido_dias": prazo_prometido,
            "dias_decorridos_entrega": dias_decorridos,
            "status": status_logistico,
            "status_pagamento": "NENHUMA_COBRANÇA"
        }
        
        print(f"⚡ Auto-Dispute: Pacote {codigo_rastreio} da Shopify processado autonomamente. Estado: {status_logistico}")
        return {"sucesso": True, "dados_encomenda": resultado_processamento}
        
    except Exception as e:
        print(f"❌ Erro crítico no processador autónomo de webhook: {e}")
        return {"sucesso": False, "erro": str(e)}
