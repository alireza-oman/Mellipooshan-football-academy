from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()

# Rate Limiter برای جلوگیری از حملات Brute Force و DDoS
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = "لطفاً برای دسترسی به این صفحه ابتدا وارد حساب خود شوید."
login_manager.login_message_category = "info"

# فعال‌سازی قوی‌ترین سطح محافظت نشست (جلوگیری از سرقت Session با جعل IP/User-Agent)
login_manager.session_protection = 'strong'