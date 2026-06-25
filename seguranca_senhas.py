import re

print("--- MÓDULO AUXILIAR: ESCUDO DE VALIDAÇÃO DE CREDENCIAIS ---")

def validar_senha_forte(password: str) -> bool:
    """
    Filtro industrial independente para garantir o padrão 
    internacional de senhas (Padrão Udemy / OWASP).
    """
    if len(password) < 8:
        print("❌ Erro de Segurança: A senha deve ter no mínimo 8 caracteres.")
        return False
    if not re.search(r"[A-Z]", password):
        print("❌ Erro de Segurança: A senha deve conter pelo menos uma letra maiúscula.")
        return False
    if not re.search(r"[a-z]", password):
        print("❌ Erro de Segurança: A senha deve conter pelo menos uma letra minúscula.")
        return False
    if not re.search(r"[0-9]", password):
        print("❌ Erro de Segurança: A senha deve conter pelo menos um número.")
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        print("❌ Erro de Segurança: A senha deve conter pelo menos um caractere especial.")
        return False
    return True
