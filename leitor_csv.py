import csv

print("--- LENDO ARQUIVO CSV DA SHOPIFY COM AIRBAG DE INFRAESTRUTURA ---")

# Abre o arquivo em modo de leitura com codificação segura
with open("dados_shopify.csv", mode="r", encoding="utf-8") as arquivo:
    leitor = csv.DictReader(arquivo)
    
    for linha in leitor:
        id_encomenda = linha.get("id", "Desconhecido").strip()
        codigo = linha.get("codigo_rastreio", "").strip()
        transportadora = linha.get("transportadora", "").strip()
        
        # ⚙️ O ESCUDO DE PROTEÇÃO CONTRA DADOS CORROMPIDOS OU NULOS
        try:
            # Validação crítica: Se faltar a transportadora ou o código, força o erro
            if not transportadora or not codigo:
                raise KeyError("Dados essenciais ('codigo_rastreio' ou 'transportadora') ausentes.")
            
            # Converte os números capturando falhas se o cliente digitar letras onde devia ser número
            prazo = int(linha["prazo_prometido_dias"])
            decorrido = int(linha["dias_decorridos_entrega"])
            
            # Aplica a nossa regra matemática de atraso
            if decorrido > prazo:
                print(f"🚨 Alerta {id_encomenda}: Código {codigo} ATRASADO por {decorrido - prazo} dias!")
            else:
                print(f"✅ Sucesso {id_encomenda}: Código {codigo} entregue no prazo.")
                
        except (KeyError, ValueError) as erro_especifico:
            print(f"🚨 Falha detectada na {id_encomenda}: Dados incompletos ou corrompidos!")
            
            # Registra o histórico da falha de forma automática no arquivo de logs
            with open("historico_erros.log", mode="a", encoding="utf-8") as ficheiro_log:
                ficheiro_log.write(f"Falha no processamento da {id_encomenda}: {erro_especifico}\n")
                
            print(f"📝 Nota de Engenharia: Erro guardado em 'historico_erros.log'. Avançando...")
            continue
