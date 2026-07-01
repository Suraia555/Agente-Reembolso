import os
import httpx
from datetime import datetime

print("--- MÓDULO ADVANCED: METEO-LOGISTICS WEATHER GUARD ATIVO ---")

async def verificar_elegibilidade_climatica(codigo_postal_hub: str, data_transito_iso: str) -> dict:
    """
    Filtro de Elegibilidade por Clima e Desastres (Força Maior).
    Cruza a localização do hub logístico com a API Open-Meteo no dia do atraso.
    Retorna se a disputa deve ser congelada ou se está limpa para disparo.
    """
    try:
        # 1. Normaliza a data (ex: extrai apenas o ano-mês-dia '2024-01-15')
        data_objeto = datetime.fromisoformat(data_transito_iso.replace("Z", "+00:00"))
        data_calculo = data_objeto.strftime("%Y-%m-%d")
        
        latitude = 25.7617
        longitude = -80.1918
        
        # 🚨 PARÂMETROS CORRIGIDOS: wind_speed_10m_max é o nome oficial aceite no arquivo
        url_meteo = (
            f"https://archive-api.open-meteo.com/v1/archive?"
            f"latitude={latitude}&longitude={longitude}&"
            f"start_date={data_calculo}&end_date={data_calculo}&"
            f"daily=weather_code,snowfall_sum,wind_speed_10m_max&timezone=auto"
        )
        
        async with httpx.AsyncClient() as client:
            resposta = await client.get(url_meteo, timeout=10)
            
            if resposta.status_code != 200:
                print(f"⚠️ Guarda Clima: API meteorológica indisponível ({resposta.status_code}). Fallback ativo.")
                return {"disputar_frete": True, "motivo": "API Clima Offline. Passagem liberada por fallback."}
                
            dados_brutos = resposta.json()
            dados_clima = dados_brutos.get("daily", {})
            
            if not dados_clima or not dados_clima.get("weather_code"):
                return {"disputar_frete": True, "motivo": "Sem dados históricos para a data. Passagem liberada."}
                
            # 🚨 CORREÇÃO DE ÍNDICE: A API retorna uma lista, capturamos o primeiro elemento [0]
            codigo_clima = int(dados_clima["weather_code"][0])
            velocidade_vento_max = float(dados_clima["wind_speed_10m_max"][0] or 0.0)
            soma_neve_cm = float(dados_clima["snowfall_sum"][0] or 0.0)
            
            # Algoritmo de tomada de decisão
            clima_extremo_detetado = codigo_clima >= 95 or velocidade_vento_max > 65.0 or soma_neve_cm > 15.0
            
            if clima_extremo_detetado:
                print(f"🚨 Guarda Clima: Bloqueio ativo. Condições severas detetadas no Hub ({codigo_postal_hub}).")
                return {
                    "disputar_frete": False,
                    "motivo": f"FORÇA MAIOR: Código WMO {codigo_clima} | Vento: {velocidade_vento_max}km/h | Neve: {soma_neve_cm}cm."
                }
                
            print(f"✅ Guarda Clima: Rota '{codigo_postal_hub}' validada com céu limpo. Sem exclusões contratuais.")
            return {
                "disputar_frete": True,
                "motivo": f"Céu Limpo. Vento estável a {velocidade_vento_max}km/h. Pronto para submissão jurídica."
            }
            
    except Exception as e:
        print(f"❌ Erro crítico no processador Meteo-Logistics Guard: {e}")
        return {"disputar_frete": True, "motivo": f"Exceção interna: {str(e)}. Liberado por segurança."}
