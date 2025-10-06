from flask import Flask
from flasgger import Swagger
from dotenv import load_dotenv

load_dotenv()

from config import Config
from blueprints import register_blueprints
from middlewares.error_handlers import register_error_handlers
from middlewares.jwt_auth import jwt, check_jwt_authentication, refresh_jwt



app = Flask(__name__)

app.config.from_object(Config)
jwt.init_app(app)
register_blueprints(app)
register_error_handlers(app)

app.before_request(check_jwt_authentication)
app.after_request(refresh_jwt)

swagger = Swagger(app, template_file="docs/swagger.yml")

if __name__ == "__main__":
    app.run()