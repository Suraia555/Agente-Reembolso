import os
import httpx
from datetime import datetime, timedelta

print("--- MÓDULO ADVANCED: ANTI-SYBIL SYNTHETIC IDENTITY SHIELD ATIVO ---")

async def verificar_integridade_loja_shopify(shop_domain: str, access_token: str) -> dict:
    """
    Validador de Identidade Sintética (Anti-Espionagem).
    Analisa a API de GraphQL da Shopify caçando o tempo de vida e faturação.
    Retorna se o utilizador deve entrar em quarentena de simulação de dados.
    """
    url_graphql = f"https://{shop_domain}/admin/api/2026-01/graphql.json"
    
    headers = {
        "X-Shopify-Access-Token": access_token,
        "Content-Type": "application/json"
    }
    
    # 🎯 Query GraphQL industrial para buscar metadados de criação da loja e últimas ordens
    query = """
    {
      shop {
        createdAt
      }
      orders(first: 10) {
        edges {
          node {
            totalPriceSet {
              shopMoney {
                amount
              }
            }
          }
        }
      }
    }
    """
    
    try:
        async with httpx.AsyncClient() as client:
            resposta = await client.post(url_graphql, json={"query": query}, headers=headers, timeout=10)
            
            if resposta.status_code != 200:
                # Se a API da Shopify rejeitar a conexão, colocamos por segurança em quarentena
                print(f"⚠️ Anti-Sybil: Falha de conexão com a Shopify ({resposta.status_code}). Quarentena ativada.")
                return {"colocar_em_quarentena": True, "motivo": "Falha na validação de handshake da API."}
                
            dados_api = resposta.json().get("data", {})
            shop_info = dados_api.get("shop", {})
            orders_info = dados_api.get("orders", {}).get("edges", [])
            
            if not shop_info:
                return {"colocar_em_quarentena": True, "motivo": "Payload vazio ou loja inexistente."}
                
            # 1. VALIDAÇÃO 1: Tempo de vida da loja (Mínimo de 3 meses / 90 dias)
            created_at_str = shop_info.get("createdAt", "")
            # Trunca o formato ISO da Shopify (ex: 2026-03-25T14:00:00Z) para objeto datetime do Python
            data_criacao_loja = datetime.fromisoformat(created_at_str.replace("Z", "+00:00"))
            data_limite = datetime.now(data_criacao_loja.tzinfo) - timedelta(days=90)
            
            loja_muito_recente = data_criacao_loja > data_limite
            
            # 2. VALIDAÇÃO 2: Faturação Histórica (Verifica se as últimas ordens têm valor real)
            total_faturado_amostra = 0.0
            for edge in orders_info:
                valor = edge.get("node", {}).get("totalPriceSet", {}).get("shopMoney", {}).get("amount", "0.0")
                total_faturado_amostra += float(valor)
                
            loja_sem_faturacao = total_faturado_amostra <= 0.0
            
            # 🔥 SELETOR DE DEFENSA CIBERNÉTICA: Se for muito recente ou tiver zero vendas, ativa o Honeypot!
            if loja_muito_recente or loja_sem_faturacao:
                print(f"🚨 Escudo Ativo: Loja '{shop_domain}' identificada como perfil sintético/espião. Quarentena ativada.")
                return {
                    "colocar_em_quarentena": True,
                    "motivo": f"Tempo de vida: {data_criacao_loja.strftime('%Y-%m-%d')} | Amostra de faturamento: ${total_faturado_amostra:.2f}"
                }
                
            print(f"✅ Anti-Sybil: Loja '{shop_domain}' validada com sucesso como e-commerce legítimo.")
            return {"colocar_em_quarentena": False, "motivo": "E-commerce verificado como idóneo."}
            
    except Exception as e:
        print(f"❌ Erro ao executar validação Anti-Sybil: {e}")
        # Na dúvida criptográfica, tranca o acesso real e simula os dados
        return {"colocar_em_quarentena": True, "motivo": f"Erro interno de exceção: {str(e)}"}
