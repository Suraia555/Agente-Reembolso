# 1. CRIANDO UMA LISTA [] DE DICIONÁRIOS {} (Múltiplas encomendas juntas)
lista_encomendas = [
    {
        "id": "ENC-001",
        "codigo_rastreio": "BR987654321",
        "transportadora": "Correios",
        "prazo_prometido_dias": 5,
        "dias_decorridos_entrega": 8  # Atrasou!
    },
    {
        "id": "ENC-002",
        "codigo_rastreio": "BR112233445",
        "transportadora": "Jadlog",
        "prazo_prometido_dias": 10,
        "dias_decorridos_entrega": 7  # No prazo.
    },
    {
        "id": "ENC-003",
        "codigo_rastreio": "BR998877665",
        "transportadora": "Loggi",
        "prazo_prometido_dias": 4,
        "dias_decorridos_entrega": 6  # Atrasou!
    }
]

print("--- PROCESSANDO BANCO DE DADOS LOCAL ---")

# 2. O LOOP (Varre cada ficha técnica dentro da lista automaticamente)
for encomenda in lista_encomendas:
    
    # 3. A REGRA DE NEGÓCIO MATEMÁTICA (if/else)
    prazo = encomenda["prazo_prometido_dias"]
    decorrido = encomendadiaz = encomenda["dias_decorridos_entrega"]
    
    if decorrido > prazo:
        status = "ELEGÍVEL PARA REEMBOLSO (Atrasado)"
        # Calcula quantos dias de atraso para a IA usar na carta
        dias_atraso = decorrido - prazo
        print(f"🚨 Alerta {encomenda['id']}: {status} por {dias_atraso} dias de atraso!")
    else:
        status = "No Prazo"
        print(f"✅ Sucesso {encomenda['id']}: Entrega realizada dentro do prazo.")
