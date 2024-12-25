from flask_jwt_extended import create_access_token,create_refresh_token
from datetime import timedelta

def Login(username:str, password:str) -> dict:

    # validação dos dados do login

    return create_credentials(username), 200

def create_credentials(username:str) -> dict:

    access_token = create_access_token(identity=username, expires_delta=timedelta(minutes=10))

    refresh_token = create_refresh_token(identity=username)

    return {'access_token': access_token, 'refresh_token': refresh_token}