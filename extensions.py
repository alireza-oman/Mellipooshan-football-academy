from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()


login_manager.login_view = 'auth.login'
login_manager.login_message = "لطفاً برای دسترسی به این صفحه ابتدا وارد سایت شوید."
login_manager.login_message_category = "info"