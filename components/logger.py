import colorlog
import logging


def handler_log():
    """
    Cria e retorna um handler de logging para saída em console com formatação colorida.
    O handler utiliza colorlog.ColoredFormatter para aplicar cores aos níveis de log
    e formata as mensagens no padrão:
        "%(log_color)s %(asctime)s | %(levelname)s - %(message)s"
    com data/hora no formato "%Y-%m-%d %H:%M:%S".
    Configurações específicas:
    - Mapeamento de cores por nível: DEBUG->cyan, INFO->green, WARNING->yellow, ERROR->red, CRITICAL->bold_red.
    - Handler retornado: logging.StreamHandler com o formatter colorido aplicado.
    Retorno:
        logging.Handler -- um StreamHandler pronto para ser adicionado a um logger.
    Observações:
    - Requer o módulo externo colorlog disponível no ambiente.
    - Não recebe parâmetros. Qualquer erro relacionado à ausência ou falha do colorlog será propagado.
    """

    log_format = "%(log_color)s %(asctime)s | %(levelname)s - %(message)s"

    log_colors = {
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    }

    color_formatter = colorlog.ColoredFormatter(
        log_format, log_colors=log_colors, datefmt="%Y-%m-%d %H:%M:%S"
    )

    handler = logging.StreamHandler()

    handler.setFormatter(color_formatter)

    return handler


def log_formatter(name: str):
    """
    Configura e retorna um logger com um manipulador de logs padrão.
    Esta função obtém um logger pelo nome fornecido, define seu nível para DEBUG
    e adiciona o handler retornado por handler_log(). É útil para padronizar
    a configuração de logging em diferentes componentes da aplicação.
    Parâmetros:
        name (str): Nome do logger a ser obtido/configurado.
    Retorna:
        logging.Logger: Instância do logger configurado (com nível DEBUG e handler adicionado).
    Efeitos colaterais:
        - Adiciona um handler ao logger em cada chamada. Chamar repetidamente com o
          mesmo nome pode resultar em handlers duplicados e em mensagens de log
          repetidas.
        - O handler é obtido chamando handler_log(); se essa função lançar uma
          exceção, ela será propagada.
    Observações:
        - Não realiza verificação para evitar handlers duplicados. Se desejar evitar
          duplicatas, verifique logger.handlers antes de adicionar um novo handler.
    """

    logger = logging.getLogger(name)

    logger.setLevel(logging.DEBUG)

    logger.addHandler(handler_log())

    return logger


logger = log_formatter(__name__)
