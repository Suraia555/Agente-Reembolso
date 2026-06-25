import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Inicializa o cliente isolado para o módulo de IA
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def gerar_carta_contestacao_ia(codigo_rastreio: str, transportadora: str) -> str:
    """
    Motor de IA de Alta Performance do CarrierRefund.
    Gera contestações jurídicas blindadas contra a alucinação de dados.
    """
    try:
        resposta = openai_client.chat.completions.create(
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
        # Retorna um fallback seguro estruturado para não quebrar a execução do lote
        return f"ERROR_IA_GENERATION_FAILED: {str(e)}"
