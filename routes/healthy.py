# Flask
from flask import request
from flask_restx import Namespace, Resource

api = Namespace("healthy", "Rotas destinadas apenas para o teste de conexão com a API")


@api.route("")
class TestResource(Resource):
    """
    Recurso de verificação de integridade (health check) da API.
    Esta classe expõe um endpoint no namespace 'api' (rota base, string vazia) para
    testar o funcionamento dos principais métodos HTTP. Cada método retorna um
    JSON simples com uma mensagem indicando que a API está saudável, juntamente
    com o status HTTP 200.
    Métodos suportados:
    - get(self):     Retorna mensagem indicando que o método GET está funcionando.
    - post(self):    Retorna mensagem indicando que o método POST está funcionando.
    - put(self):     Retorna mensagem indicando que o método PUT está funcionando.
    - delete(self):  Retorna mensagem indicando que o método DELETE está funcionando.
    - patch(self):   Retorna mensagem indicando que o método PATCH está funcionando.
    Uso típico:
    - Empregado como endpoint de smoke tests / health checks para monitoramento e
        validação básica de disponibilidade da API.
    - Respostas intencionais simples para facilitar testes automatizados e manuais.
    Observações:
    - Todas as respostas retornam código HTTP 200.
    - Pode ser estendido para incluir checks mais detalhados (ex.: dependências de
        banco, fila, serviços externos) conforme necessidade.
    """

    def get(self):
        return {"message": "API is healthy and get method is working"}, 200

    def post(self):
        return {"message": "API is healthy and post method is working"}, 200

    def put(self):
        return {"message": "API is healthy and put method is working"}, 200

    def delete(self):
        return {"message": "API is healthy and delete method is working"}, 200

    def patch(self):
        return {"message": "API is healthy and patch method is working"}, 200
