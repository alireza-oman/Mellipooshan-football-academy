from flask import Blueprint

panel_bp = Blueprint('panel', __name__, url_prefix='/panel')

from . import routes