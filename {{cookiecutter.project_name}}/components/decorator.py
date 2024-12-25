# Flask
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

# Externas
from functools import wraps

# Componentes
from components.logger import logger

def decorator_main(token:bool=True):

    def decorator_validate(function):

        @wraps(function)

        def wrapper(args):

            if token:

                status_token = validate_token()

                if not status_token['status']:

                    return {'message': 'user not logged'}, 401
                
                return function(args)
            
            return function(args)
        
        return wrapper
    
    return decorator_validate


def validate_token() -> dict:

    try:

        try:
            # Tentando com a token normal
            verify_jwt_in_request()
        except:
            # Tentando com a refresh token
            verify_jwt_in_request(refresh=True)

        logger.debug("Token valida")

        return {'status': True, 'message': 'Token válida'}
    
    except Exception as e:

        logger.error("Token invalida")

        return {'status': False, 'message': str(e)}