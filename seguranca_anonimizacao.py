import hashlib

print("--- MÓDULO DE SEGURANÇA: CRIPTOGRAFIA E ANONIMIZAÇÃO ATIVO ---")

def gerar_hash_email_lista_negra(email: str) -> str:
    """
    Transforma o e-mail em um Hash SHA-256 irreversível de 64 caracteres.
    'cliente_calote@gmail.com' vira '8f93a1...'. Não há como desfazer o processo.
    """
    email_limpo = email.strip().lower() # Normaliza para evitar burlas com letras maiúsculas
    hash_objeto = hashlib.sha256(email_limpo.encode('utf-8'))
    return hash_objeto.hexdigest()
