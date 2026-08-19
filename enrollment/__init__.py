from flask import Blueprint

enrollment_bp = Blueprint('enrollment', __name__, url_prefix='/enrollment')

from enrollment import routes