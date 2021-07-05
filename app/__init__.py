from flask import Flask

from app.config import Config

import app.context as ctx

server = Flask(__name__, static_folder="../front/dist/static")
server.config.from_object('app.config.Config')

ctx.init(server)

from app.models.configurations import Configurations

ctx.db.create_all()

from app.api import vpn_bp
from app.api import check_bp

server.register_blueprint(vpn_bp)
server.register_blueprint(check_bp)

server.logger.info('>>> {}'.format(Config.FLASK_ENV))

server.logger.info(server.url_map)
