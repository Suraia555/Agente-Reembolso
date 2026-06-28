import os
from dotenv import load_dotenv
from supabase import create_client, Client
from openai import OpenAI

load_dotenv()

# Inicializa os motores isolados para o módulo de suporte RAG
supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

print("--- MÓDULO ENTERPRISE: CARRIERREFUND AI COPILOT ATIVO ---")

def gerar_coordenadas_vetoriais(texto: str) -> list:
    """
    Transforma uma string de texto em um vetor matemático de 1536 dimensões
    utilizando o motor de embutimento de alta performance da OpenAI.
    """
    try:
        resposta = openai_client.embeddings.create(
            model="text-embedding-3-small",
            input=[texto.strip()]
        )
        return resposta.data[0].embedding
    except Exception as e:
        print(f"❌ Erro ao gerar vetor matemático: {e}")
        return []

async def executar_consulta_rag_copilot(pergunta_usuario: str, idioma_alvo: str = "en") -> str:
    """
    Core RAG System: Transforma a pergunta em vetor, caça o contexto exato
    no Supabase via RPC Vetorial e responde usando o GPT de forma contextualizada.
    """
    try:
        # A. Transforma a dúvida do lojista gringo em coordenadas
        vetor_pergunta = gerar_coordenadas_vetoriais(pergunta_usuario)
        if not vetor_pergunta:
            return "ERROR_VECTOR_GENERATION_FAILED"
            
        # B. Dispara a busca vetorial por similaridade de cosseno dentro do PostgreSQL
        resposta_rpc = supabase.rpc("buscar_artigos_suporte", {
            "vetor_busca": vetor_pergunta,
            "limite_resultados": 2, # Puxa os 2 artigos mais relevantes para economizar tokens
            "idioma_alvo": idioma_alvo
        }).execute()
        
        artigos_localizados = resposta_rpc.data
        contexto_documentos = ""
        
        if artigos_localizados:
            for artigo in artigos_localizados:
                contexto_documentos += f"\n--- Artigo: {artigo['titulo']} ---\n{artigo['conteudo']}\n"
        else:
            contexto_documentos = "Nenhum documento específico localizado na base de dados para esta dúvida."
            
        # C. Alimenta o modelo de Chat com o contexto real extraído da tua base de dados
        resposta_ia = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system", 
                    "content": (
                        f"You are the official AI Copilot for CarrierRefund platform. "
                        f"Answer the user's question accurately based ONLY on the provided context below. "
                        f"Write your response in the requested language language: '{idioma_alvo}'.\n"
                        f"Context from internal database:\n{contexto_documentos}"
                    )
                },
                {"role": "user", "content": pergunta_usuario}
            ]
        )
        
        return respuesta_ia.choices[0].message.content
        
    except Exception as e:
        print(f"❌ Erro crítico no motor RAG do Copilot: {e}")
        return f"ERROR_COPILOT_FAILED: {str(e)}"
