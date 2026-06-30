import time
import random
from datetime import datetime

print("--- MÓDULO ADVANCED: SMART DELAY PROFILING ENGINE ATIVO ---")

def calcular_pausa_comportamental_teoria_jogos() -> float:
    """
    Algoritmo baseado em Teoria dos Jogos.
    Analisa o fuso horário de tráfego logístico e calcula uma pausa aleatória
    em segundos para mimetizar o comportamento de um operador humano.
    """
    try:
        hora_atual_local = datetime.now().hour
        
        # 📊 MODELAÇÃO DE TRÁFEGO: Define a janela de comportamento
        # Se for horário comercial (08h às 18h), o fluxo de funcionários nos portais é alto.
        # O robô pode agir de forma ligeiramente mais rápida, camuflado no meio do tráfego real.
        if 8 <= hora_atual_local <= 18:
            # Gera um atraso fracionado e dinâmico entre 3.1 e 8.4 segundos
            tempo_espera = round(random.uniform(3.1, 8.4), 2)
            print(f"⏱️ Smart Delay: Janela Comercial Ativa. Pausa humana calculada: {tempo_espera}s.")
        else:
            # Fora do horário comercial, a segurança das transportadoras vigia acessos em massa.
            # O robô desacelera drasticamente e espalha as disputas para parecer um funcionário noturno.
            tempo_espera = round(random.uniform(12.5, 27.9), 2)
            print(f"⏱️ Smart Delay: Janela de Baixo Tráfego Noturno. Pausa de segurança estendida: {tempo_espera}s.")
            
        return tempo_espera
        
    except Exception as e:
        print(f"❌ Erro ao computar Teoria dos Jogos no gerenciador de filas: {e}")
        return 5.0 # Fallback seguro de 5 segundos se a matemática de tempo falhar

def executar_atraso_silencioso():
    """
    Bloqueia a linha de execução do worker temporariamente com base no perfil calculado,
    quebrando qualquer padrão de assinatura temporal que os firewalls procurem.
    """
    segundos_pausa = calcular_pausa_comportamental_teoria_jogos()
    time.sleep(segundos_pausa)

def injetar_mutacao_gramatical_prompt(prompt_base: str) -> str:
    """
    Adiciona instruções de variação estilística ao prompt jurídico [ENC-503].
    Força a OpenAI a reescrever a carta estruturalmente, alterando sinónimos 
    e parágrafos para que cada PDF submetido à DHL seja semanticamente único.
    """
    estilos_escrita = [
        "Use a direct corporate tone, emphasizing strict contractual deadlines.",
        "Write with a formal legal approach, prioritizing regulatory non-compliance terms.",
        "Structure the claim with a firm executive summary style, demanding immediate audit verification."
    ]
    
    estilo_aleatorio = random.choice(estilos_escrita)
    
    # Injeta a mutação ao prompt original sem quebrar a língua corporativa inglesa exigida [ENC-503]
    prompt_mutado = f"{prompt_base} {estilo_aleatorio} Ensure the syntax structure is unique compared to previous outputs."
    return prompt_mutado
