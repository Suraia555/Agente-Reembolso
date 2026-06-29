import os
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

# Inicializa o cliente ASSÍNCRONO isolado para o módulo de IA (Alta Performance em Lote)
openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def gerar_carta_contestacao_ia(codigo_rastreio: str, transportadora: str) -> str:
    """
    Motor de IA de Alta Performance do CarrierRefund.
    Gera contestações jurídicas blindadas contra a alucinação de dados.
    """
    try:
        # O 'await' nativo liberta a linha de execução enquanto a OpenAI responde
        resposta = await openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system", 
                    "content": "You are a Senior E-commerce Logistics Lawyer. Write exclusively in formal legal English. Never invent data. Start directly with the formal claim text."
                },
                {
                    "role": "user", 
                    "content": f"Draft an official claim for the package with tracking code {codigo_rastreio} handled by {transportadora} because it missed the guaranteed delivery deadline."
                }
            ]
        )
        return resposta.choices[0].message.content
    except Exception as e:
        # Mantém rigorosamente o teu fallback seguro estruturado para o loop do main.py
        return f"ERROR_IA_GENERATION_FAILED: {str(e)}"
