import csv

print("--- LENDO ARQUIVO CSV DA SHOPIFY ---")

# Abre o arquivo em modo de leitura (r = read) com codificação segura
with open("dados_shopify.csv", mode="r", encoding="utf-8") as arquivo:
    # O DictReader transforma automaticamente cada linha do CSV num Dicionário Python
    leitor = csv.DictReader(arquivo)
    
    for linha in leitor:
        # Extrai os dados transformando os números em Inteiros (int) para a matemática funcionar
        id_encomenda = linha["id"]
        codigo = linha["codigo_rastreio"]
        prazo = int(linha["prazo_prometido_dias"])
        decorrido = int(linha["dias_decorridos_entrega"])
        
        # Aplica a nossa regra matemática de atraso
        if decorrido > prazo:
            print(f"🚨 Alerta {id_encomenda}: Código {codigo} ATRASADO por {decorrido - prazo} dias!")
        else:
            print(f"✅ Sucesso {id_encomenda}: Código {codigo} entregue no prazo.")
