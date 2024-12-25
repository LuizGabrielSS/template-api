from routes.login import api

from flask_restx import fields

# Requisições

model_login_req = api.parser()

model_login_req.add_argument('username', location='json',required=True,type='string',help="Username to login")

model_login_req.add_argument('password', location='json',required=True,type='string',help="password to login")

# Respostas

model_login_answer = api.model('LoginResponse', {
    'access_token': fields.String(description='Access Token'),
    'refresh_token': fields.String(description='Refresh Token')
})