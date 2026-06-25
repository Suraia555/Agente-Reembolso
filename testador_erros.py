import logging

# Configuração do Logger Industrial para escrever no arquivo e exibir no terminal
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("historico_erros.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("CarrierRefund_Telemetry")

def registrar_falha_sistema(encomenda_id: str, detalhe_erro: str):
    """
    Escudo de telemetria assíncrona para capturar quebras de infraestrutura
    sem travar a thread principal de execução.
    """
    mensagem_falha = f"Falha no processamento da {encomenda_id}: {detalhe_erro}"
    logger.error(mensagem_falha)
