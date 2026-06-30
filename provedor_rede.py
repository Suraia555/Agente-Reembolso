import os
import random
from dotenv import load_dotenv
from curl_cffi.requests import AsyncSession

load_dotenv()

# 🌐 Captura as credenciais de infraestrutura de rede
PROXY_USER = os.getenv("PROXY_USERNAME")
PROXY_PASS = os.getenv("PROXY_PASSWORD")
PROXY_HOST = os.getenv("PROXY_GATEWAY_URL")

print("--- MÓDULO ADVANCED: RESIDENTIAL PROXY ROTATION ENGINE ATIVO ---")

def obter_configuracao_proxy_dinamico() -> dict:
    """
    Gera o dicionário de proxy residencial com uma sessão única aleatória.
    O parâmetro 'sess' força o provedor de proxies a mudar o IP dos EUA/Europa
    a cada nova requisição que o teu robô disparar.
    """
    # Gera um identificador aleatório para forçar a rotação instantânea do IP
    session_id = random.randint(100000, 999999)
    
    # Monta a string de autenticação padrão internacional para proxies residenciais
    # O sufixo '-sessid-' instrui a Bright Data/Oxylabs a rodar o nó de rede
    proxy_url = f"http://{PROXY_USER}-sessid-{session_id}:{PROXY_PASS}@{PROXY_HOST}"
    
    return {
        "http": proxy_url,
        "https": proxy_url
    }

async def disparar_requisicao_camuflada(url_alvo: str) -> str:
    """
    Executa uma requisição HTTP assíncrona ultra performática.
    Mascara o IP com Proxy Residencial e emula o TLS Fingerprint do Chrome.
    """
    try:
        proxies_config = obter_configuracao_proxy_dinamico()
        
        # 🕵️ Lista de User-Agents reais atualizados para simular tráfego humano
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        ]
        
        headers_humanos = {
            "User-Agent": random.choice(user_agents),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive"
        }
        
        # 🚨 O SEGREDO ANTI-BOT: AsyncSession com browser='chrome'
        # Isto faz o curl_cffi imitar as curvas criptográficas exatas do Google Chrome real,
        # cegando por completo os sistemas Akamai e Cloudflare Bot Management.
        async with AsyncSession(impersonate="chrome", proxies=proxies_config) as sessao:
            resposta = await sessao.get(url_alvo, headers=headers_humanos, timeout=15)
            
            if resposta.status_code != 200:
                print(f"⚠️ Provedor Rede: Código de status inesperado do portal: {resposta.status_code}")
                
            return resposta.text
            
    except Exception as e:
        print(f"❌ Erro fatal no motor de rotação de proxies: {e}")
        return "ERROR_PROXY_NETWORK_BLOCKED"
