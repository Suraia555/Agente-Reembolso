import sys

print("--- INICIANDO PROCESSAMENTO SEGURO COM ARQUITETURA DE LOGS ---")

# Banco de dados simulado com um erro grave na segunda ficha técnica
encomendas_clientes = [
    {"id": "ENC-001", "codigo": "BR111", "transportadora": "Correios"},
    {"id": "ENC-002", "codigo": "BR222"},  # ERRO: Falta a chave 'transportadora'!
    {"id": "ENC-003", "codigo": "BR333", "transportadora": "Loggi"}
]

# Loop para processar todas as encomendas em lote
for enc in encomendas_clientes:
    
    # ⚙️ O ESCUDO DE PROTEÇÃO (try = tenta executar / except = captura o erro)
    try:
        # O Python vai tentar ler a transportadora. Na ENC-002 ele vai falhar.
        empresa = enc["transportadora"]
        print(f"✅ Sucesso {enc['id']}: Código {enc['codigo']} enviado via {empresa} processado.")
        
    except KeyError as erro_especifico:
        # Se a chave não existir, o except impede o programa de quebrar
        print(f"🚨 Alerta Crítico na {enc['id']}: Dados incompletos ou corrompidos!")
        
        # Criando ou abrindo um arquivo físico de LOGS para registrar o histórico da falha
        with open("historico_erros.log", mode="a", encoding="utf-8") as ficheiro_log:
            ficheiro_log.write(f"Falha no processamento da {enc['id']}: Faltando o dado {erro_especifico}\n")
            
        print(f"📝 Nota de Engenharia: Erro guardado em 'historico_erros.log'. Avançando para o próximo...")
        
        # O comando 'continue' manda o loop ignorar esta falha e passar logo para a próxima encomenda
        continue
