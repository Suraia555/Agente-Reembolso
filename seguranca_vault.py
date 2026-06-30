import os
import base64
from dotenv import load_dotenv
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

load_dotenv()

# 🔐 CHAVE MESTRA DO ECOSSISTEMA: Carregada a partir do teu .env oculto
# Em ambiente Zero-Knowledge puro, esta chave pode ser derivada de uma pass-phrase do cliente.
# Para o pipeline de produção do gateway, usamos a chave de infraestrutura simétrica.
SECRET_VAULT_KEY = os.getenv("SECRET_VAULT_KEY")

print("--- MÓDULO ADVANCED: ZERO-KNOWLEDGE CRYPTO VAULT ATIVO ---")

def encriptar_credencial_transporte(texto_puro: str) -> dict:
    """
    Criptografa credenciais sensíveis (chaves de API/Senhas) usando AES-256-GCM.
    Retorna o payload, o nonce (IV) e a tag de autenticação em strings Base64 estáveis.
    """
    try:
        # 1. Converte a chave mestra em bytes (exige exatamente 32 bytes para AES-256)
        chave_bytes = base64.b64decode(SECRET_VAULT_KEY.encode('utf-8'))
        aesgcm = AESGCM(chave_bytes)
        
        # 2. Gera um Nonce (Vetor de Inicialização) aleatório e seguro de 12 bytes
        nonce = AESGCM.generate_nonce(bit_length=96)
        
        # 3. Encripta o conteúdo gerando o bloco cifrado juntamente com a tag de autenticação
        dados_encriptados_com_tag = aesgcm.encrypt(nonce, texto_puro.encode('utf-8'), None)
        
        # O algoritmo AESGCM do cryptography junta a tag nos últimos 16 bytes. Separamos cirurgicamente:
        tag_tamanho = 16
        ciphertext = dados_encriptados_com_tag[:-tag_tamanho]
        tag = dados_encriptados_com_tag[-tag_tamanho:]
        
        # 4. Transforma os binários em strings estáveis usando Base64 para gravação no Supabase
        return {
            "sucesso": True,
            "encrypted_payload": base64.b64encode(ciphertext).decode('utf-8'),
            "nonce": base64.b64encode(nonce).decode('utf-8'),
            "tag": base64.b64encode(tag).decode('utf-8')
        }
    except Exception as e:
        print(f"❌ Erro crítico na encriptação do Vault: {e}")
        return {"sucesso": False, "erro": str(e)}

def desencriptar_credencial_transporte(encrypted_payload: str, nonce_b64: str, tag_b64: str) -> str:
    """
    Reconstrói o bloco criptográfico e decifra a chave original.
    Garante integridade absoluta: se o dado for alterado na base de dados, a decifração falha.
    """
    try:
        chave_bytes = base64.b64decode(SECRET_VAULT_KEY.encode('utf-8'))
        aesgcm = AESGCM(chave_bytes)
        
        # Decodifica as strings Base64 de volta para bytes puros
        ciphertext = base64.b64decode(encrypted_payload.encode('utf-8'))
        nonce = base64.b64decode(nonce_b64.encode('utf-8'))
        tag = base64.b64decode(tag_b64.encode('utf-8'))
        
        # Reconstrói a estrutura esperada pelo motor (Ciphertext + Tag)
        dados_completos = ciphertext + tag
        
        # Decifra e retorna o texto limpo original
        texto_decifrado = aesgcm.decrypt(nonce, dados_completos, None)
        return texto_decifrado.decode('utf-8')
    except Exception as e:
        print(f"❌ Falha de integridade criptográfica no Vault: {e}")
        return "ERROR_VAULT_DECRYPTION_FAILED"
