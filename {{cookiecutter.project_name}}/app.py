# Flask
from flask import Flask,Blueprint,request
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_restx import Api
import logging

# Componentes
from components.secrets import get_secret
from components.logger import handler_log

# Rotas
from routes.login import api as login


def create_app(test_mode=False):

    app = Flask(__name__)

    app.config['JWT_SECRET_KEY'] = get_secret('jwt_secret_key')

    app.config.SWAGGER_UI_REQUEST_DURATION = True

    app.configSWAGGER_UI_OPERATION_ID = True

    app.config.TESTING = test_mode

    werkzeug_logger = logging.getLogger('werkzeug')

    werkzeug_logger.addHandler(handler_log())

    werkzeug_logger.setLevel(logging.DEBUG)

    main_route = Blueprint('api', __name__)

    api = Api(
        main_route,
        version='1.0',
        title='API',
        description='API',
        doc='/doc'
    )

    api.add_namespace(login)

    app.register_blueprint(main_route)

    CORS(app)

    return app


if __name__ == '__main__':

    app = create_app()

    app.run(
        host='0.0.0.0',
        port=3000,
        debug=True,
        use_reloader=True,
        threaded=True,
        # ssl_context=('cert.pem', 'key.pem') # Para rodar com HTTPS
    )