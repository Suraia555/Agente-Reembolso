print("--- MÓDULO DE INTERNACIONA-LIZAÇÃO: MOTOR MULTILINGUE ATIVO ---")

# Dicionário de Tradução Core para Mensagens da API (i18n)
DICIONARIO_TRADUCOES = {
    "en": {
        "erro_autenticacao": "Authentication failed. Please verify your credentials.",
        "lote_iniciado": "Starting automated batch execution for user UUID: ",
        "sucesso_upload": "File processed! Encomendas imported successfully into the cloud.",
        "bloqueio_calote": "Access suspended due to unpaid commission invoices. Please complete your payment.",
        "ia_system_prompt": "You are a Senior E-commerce Logistics Lawyer. Write exclusively in formal legal English. Never invent data. Start directly with the formal claim text."
    },
    "pt": {
        "erro_autenticacao": "Falha na autenticação. Verifique as suas credenciais.",
        "lote_iniciado": "Iniciando execução em lote automatizada para o UUID: ",
        "sucesso_upload": "Ficheiro processado! Encomendas importadas com sucesso para a nuvem.",
        "bloqueio_calote": "Acesso suspenso por faturas de comissão pendentes. Efetue o pagamento.",
        "ia_system_prompt": "Você é um Advogado Sénior de Logística de E-commerce. Escreva exclusivamente em português formal e jurídico. Nunca invente dados. Comece diretamente com o texto formal da reclamação."
    },
    "es": {
        "erro_autenticacao": "Fallo de autenticación. Por favor, verifique sus credenciales.",
        "lote_iniciado": "Iniciando la ejecución por lotes automatizada para el UUID: ",
        "sucesso_upload": "¡Archivo procesado! Pedidos importados con éxito a la nube.",
        "bloqueio_calote": "Acceso suspendido debido a facturas de comisiones pendientes. Por favor complete su pago.",
        "ia_system_prompt": "Usted es un Abogado Senior de Logística de Comercio Electrónico. Escriba exclusivamente en español formal y legal. Nunca invente datos. Comience directamente con el texto formal de la reclamación."
    },
    "fr": {
        "erro_autenticacao": "Échec de l'authentification. Veuillez vérifier vos identifiants.",
        "lote_iniciado": "Démarrage de l'exécution automatique par lot pour l'UUID utilisateur : ",
        "sucesso_upload": "Fichier traité ! Commandes importées avec succès dans le cloud.",
        "bloqueio_calote": "Accès suspendu en raison de factures de commission impayées. Veuillez compléter votre paiement.",
        "ia_system_prompt": "Vous êtes un Avocat Senior en Logistique de E-commerce. Écrivez exclusivement en français formel et juridique. N'inventez jamais de données. Commencez directement par le texte formel de la réclamation."
    }
}

def detetar_idioma_requisicao(accept_language_header: str) -> str:
    """
    Interpola os cabeçalhos HTTP globais (Accept-Language) enviados pelo navegador
    e extrai o idioma principal se estiver mapeado no sistema (EN, PT, ES, FR).
    Se o cliente usar outra língua (ex: Alemão), o fallback padrão é 'en' (Inglês).
    """
    if not accept_language_header:
        return "en"
        
    # Divide os cabeçalhos por vírgula e limpa os espaços (Ex: "pt-BR,pt;q=0.9,en;q=0.8")
    idiomas_solicitados = [lang.strip().split("-")[0].split(";")[0].lower() for lang in accept_language_header.split(",")]
    
    for lang in idiomas_solicitados:
        if lang in DICIONARIO_TRADUCOES:
            return lang
            
    return "en" # Fallback internacional robusto

def obter_texto_traduzido(chave: str, idioma: str) -> str:
    """
    Garante o retorno seguro da string traduzida sem risco de KeyError.
    """
    idioma_alvo = idioma if idioma in DICIONARIO_TRADUCOES else "en"
    return DICIONARIO_TRADUCOES[idioma_alvo].get(chave, DICIONARIO_TRADUCOES["en"].get(chave, ""))
