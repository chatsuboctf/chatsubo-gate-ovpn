from flask import Blueprint
from flask_restx import Api

vpn_bp = Blueprint('vpn_bp', __name__, url_prefix='/api/vpn')
check_bp = Blueprint('check_bp', __name__, url_prefix='/api/check')

vpn_api = Api(vpn_bp)
check_api = Api(check_bp)

# Import resources to ensure view is registered
from .vpn import *
from .check import *
