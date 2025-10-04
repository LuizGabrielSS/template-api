from datetime import datetime
from functools import wraps

from components.logger import logger

def timer(func_name:str):

    def calculate_time(function):

        @wraps(function)

        def wrapper(*args, **kwargs):

            start = datetime.now()

            logger.info(f"Iniciando {func_name}")

            result = function(*args, **kwargs)

            logger.info(f'{func_name} finalizado em {datetime.now() - start}')

            return result
        
        return wrapper
    
    return calculate_time