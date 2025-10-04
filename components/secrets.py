import os
from typing import Union

from components.logger import logger


def get_secret(secret_key: str) -> Union[str, bool]:

    # Validando que recebeu uma secret key
    if not secret_key:
    
        logger.error("Chave de senha não fornecida")
    
        return False
    
    if os.getenv(secret_key) is not None:

        logger.debug(f"{secret_key} encontrada com sucesso")

        return os.getenv(secret_key)

    try:

        with open(f'private/{secret_key}') as f:

            logger.debug(f"{secret_key} encontrada com sucesso")
        
            return f.read().strip()
        
    except FileNotFoundError:

        logger.error(f"{secret_key} não encontrado")
    
        return False
    
    except Exception as e:

        logger.error(f"Erro ao tentar abrir {secret_key}: {e}")
    
        return False