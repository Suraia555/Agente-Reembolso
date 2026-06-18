import os
from dotenv import load_dotenv
from openai import OpenAI

# 1. Carrega a chave de segurança do arquivo oculto .env
load_dotenv()

# 2. Inicializa o cliente oficial da OpenAI
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# 3. A Função Modular para capturar os dados do cliente no terminal
def processar_encomenda():
    print("--- INICIANDO MOTOR DE REGISTO ---")
    codigo = input("Digite o código de rastreio: ")
    transportadora = input("Digite o nome da transportadora: ")
    return codigo, transportadora

# 4. Executa a função e guarda os dados digitados em variáveis globais
codigo_final, transportadora_final = processar_encomenda()

print("--- SOLICITANDO CARTA DE REEMBOLSO COM IA ---")

# 5. Dispara os dados dinâmicos para o cérebro da IA (GPT-4o mini)
try:
    resposta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system", 
                "content": "You are a Senior E-commerce Logistics Lawyer. Write exclusively in formal legal English. Never invent data. Do not include conversational text. Start directly with the formal claim text."
            },
            {
                "role": "user", 
                "content": f"Draft an official claim for the package with tracking code {codigo_final} handled by {transportadora_final} because it missed the guaranteed delivery deadline."
            }
        ]
    )
    # Exibe a carta final gerada se a chave for real
    print(resposta.choices[0].message.content)

except Exception as e:
    # Captura o erro controlado devido à chave de testes sk-test
    print(f"Erro detetado (Esperado devido à chave de testes): {e}")
