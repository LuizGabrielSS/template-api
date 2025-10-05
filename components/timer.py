from datetime import datetime
from functools import wraps

from components.logger import logger


def timer(func_name: str):
    """
    Decorator de cronômetro para medir e logar o tempo de execução de funções.
    Parâmetros:
        func_name (str): Nome descritivo usado nas mensagens de log para identificar a função.
    Retorna:
        Callable: Um decorator que, quando aplicado a uma função, realiza as seguintes ações:
            - Registra uma mensagem de início no logger: "Iniciando {func_name}".
            - Executa a função decorada e captura seu resultado.
            - Registra uma mensagem de término com o tempo decorrido: "{func_name} finalizado em {duração}".
            - Retorna o resultado original da função decorada.
    Observações:
        - Presume-se que 'logger', 'datetime' e 'wraps' estejam disponíveis no escopo onde o decorator é utilizado.
        - Mantém a assinatura e o comportamento da função decorada, apenas adicionando logging e medição de tempo.
    """

    def calculate_time(function):

        @wraps(function)
        def wrapper(*args, **kwargs):

            start = datetime.now()

            logger.info(f"Iniciando {func_name}")

            result = function(*args, **kwargs)

            logger.info(f"{func_name} finalizado em {datetime.now() - start}")

            return result

        return wrapper

    return calculate_time
