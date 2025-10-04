# Flask
from flask import request
from flask_restx import Namespace, Resource

api = Namespace('healthy','Rotas destinadas apenas para o teste de conexão com a API')

@api.route('')
class TestResource(Resource):
    def get(self):
        return {'message':'API is healthy and get method is working'}, 200
    
    def post(self):
        return {'message':'API is healthy and post method is working'}, 200
    
    def put(self):
        return {'message':'API is healthy and put method is working'}, 200

    def delete(self):
        return {'message':'API is healthy and delete method is working'}, 200

    def patch(self):
        return {'message':'API is healthy and patch method is working'}, 200