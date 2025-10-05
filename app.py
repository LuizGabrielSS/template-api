# Flask
from flask import Flask, Blueprint, request
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_restx import Api
import logging

# Componentes
from components.secrets import get_secret
from components.logger import handler_log

# Routes
from routes.healthy import api as healthy


def handle_app(testing=False):
    """
    Inicializa e configura a aplicação Flask.
    Parâmetros
    ----------
    testing : bool, opcional
        Se True, ativa o modo de teste da aplicação (padrão: False).
    Retorna
    -------
    Flask
        Instância da aplicação Flask configurada e pronta para uso.
    Descrição
    ---------
    Esta função monta e retorna uma aplicação Flask com as configurações e integrações necessárias para a API:
    - Cria a instância Flask.
    - Define a chave secreta do JWT obtida via get_secret('jwt_secret_key').
    - Ativa opções da interface Swagger (SWAGGER_UI_REQUEST_DURATION e SWAGGER_UI_OPERATION_ID).
    - Seta a flag de TESTING conforme o parâmetro.
    - Configura o logger 'werkzeug' adicionando um handler (handler_log()) e ajustando o nível para DEBUG.
    - Adiciona o namespace da API (healthy).
    - Cria um Blueprint chamado 'api' e instancia um objeto Api com metadata (version, title, description e rota de documentação '/doc').
    - Registra o blueprint na aplicação.
    - Habilita CORS para a aplicação.
    - Inicializa o JWTManager com a aplicação.
    Efeitos colaterais
    ------------------
    - Lê segredos externos (get_secret).
    - Modifica o logger global 'werkzeug'.
    - Registra blueprints e namespaces na aplicação Flask.
    Erros
    -----
    Podem ser propagadas exceções originadas por get_secret, pela criação/configuração dos componentes (handler_log, Api, CORS, JWTManager) ou por falhas na inicialização do Flask.
    """

    app = Flask(__name__)

    app.config["JWT_SECRET_KEY"] = get_secret("jwt_secret_key")

    app.config.SWAGGER_UI_REQUEST_DURATION = True

    app.config.SWAGGER_UI_OPERATION_ID = True

    app.config.TESTING = testing

    werkzeug_logger = logging.getLogger("werkzeug")

    werkzeug_logger.addHandler(handler_log())

    werkzeug_logger.setLevel(logging.DEBUG)

    api.add_namespace(healthy)

    main_route = Blueprint("api", __name__)

    api = Api(main_route, version="1.0", title="API", description="API", doc="/doc")

    app.register_blueprint(main_route)

    CORS(app)

    JWTManager(app)

    return app


if __name__ == "__main__":

    app = handle_app()

    app.run(
        host="0.0.0.0",
        port=3000,
        debug=True,
        use_reloader=True,
        threaded=True,
        # ssl_context=('cert.pem', 'key.pem') # Para rodar com HTTPS
    )
