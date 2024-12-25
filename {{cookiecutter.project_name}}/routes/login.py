# Flask
from flask import request
from flask_restx import Namespace, Resource

# Funções
from src.login import Login

# Decorator
from components.decorator import decorator_main

api = Namespace('login','Rotas destinadas ao login e refresh da token')

from models.login import model_login_req,model_login_answer


@api.route("")
class LoginSystem(Resource):
    @decorator_main(False)
    @api.expect(model_login_req)
    @api.response(200,"success",model_login_answer)
    @api.doc(id="Login na api")
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        # Verifica se o usuário e senha estão preenchidos
        if not username or not password:
            return {'message': 'Usuário ou senha inválidos'}, 400
        
        return Login(username, password)
    
