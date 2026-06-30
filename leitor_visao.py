import os
import base64
import json
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

# Inicializa o cliente ASSÍNCRONO isolado para o motor de Visão Computacional
openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

print("--- MÓDULO ADVANCED: MULTI-LAYER VISION OCR ENGINE ATIVO ---")

def converter_imagem_para_base64(caminho_imagem: str) -> str:
    """
    Lê um ficheiro de imagem local em modo binário e converte-o 
    numa string Base64 estável para transmissão na API da OpenAI.
    """
    try:
        with open(caminho_imagem, "rb") as arquivo_imagem:
            binario = arquivo_imagem.read()
            return base64.b64encode(binario).decode("utf-8")
    except Exception as e:
        print(f"❌ Erro ao decodificar imagem para Base64: {e}")
        return ""

async def extrair_dados_comprovativo_visao(caminho_imagem_pod: str) -> dict:
    """
    Motor OCR Multicamada por Visão Computacional.
    Analisa visualmente a captura de ecrã do POD (Proof of Delivery),
    extrai os carimbos de tempo e valida se existe assinatura visível.
    """
    try:
        # 1. Converte o ficheiro local na memória RAM
        imagem_b64 = converter_imagem_para_base64(caminho_imagem_pod)
        if not imagem_b64:
            raise Exception("Ficheiro de imagem inválido ou inacessível.")
            
        # 2. Chamada assíncrona pura ao motor multimodal gpt-4o-mini
        # Forçamos a resposta a vir em JSON estruturado nativo para evitar alucinações
        resposta = await openai_client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert logistics document analyzer. Analyze the provided image of a Proof of Delivery (POD). "
                        "Extract the exact delivery date, delivery time, and determine if a signature or stamp is physically visible. "
                        "Respond exclusively in a compact JSON object with the following keys: "
                        "'data_entrega' (string or null), 'hora_entrega' (string or null), 'assinatura_presente' (boolean)."
                    )
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text", 
                            "text": "Extract the delivery timestamp and signature validation from this proof of delivery screenshot."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{imagem_b64}",
                                "detail": "high"  # Força resolução máxima para ler letras pequenas e assinaturas rasuradas
                            }
                        }
                    ]
                }
            ]
        )
        
        # 3. Faz o parse do JSON seguro recebido da inteligência artificial
        conteudo_bruto = resposta.choices[0].message.content
        dados_estruturados = json.loads(conteudo_bruto)
        
        print(f"👁️ Vision OCR: Extração visual concluída com sucesso para o arquivo.")
        return {
            "sucesso": True,
            "dados_extraidos": dados_estruturados
        }
        
    except Exception as e:
        print(f"❌ Erro crítico no processador de Visão Computacional OCR: {e}")
        return {
            "sucesso": False,
            "erro": str(e),
            "dados_extraidos": {
                "data_entrega": None,
                "hora_entrega": None,
                "assinatura_presente": False
            }
        }
