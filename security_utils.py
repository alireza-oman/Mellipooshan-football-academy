import os
import re
import uuid
from functools import wraps
from urllib.parse import urlsplit
from flask import abort, request, current_app
from flask_login import current_user
from werkzeug.utils import secure_filename

# الگوی خام برای اعتبارسنجی فرم‌های WTForms
PHONE_REGEX = r'^09\d{9}$'

# الگوی کامپایل‌شده برای استفاده در توابع داخلی
IRAN_PHONE_REGEX = re.compile(PHONE_REGEX)


def validate_iran_phone(phone: str) -> bool:
    """بررسی فرمت شماره موبایل معتبر ایران"""
    if not phone:
        return False
    return bool(IRAN_PHONE_REGEX.match(phone.strip()))


def validate_national_code(code: str) -> bool:
    """الگوریتم رسمی صحت‌سنجی رقم کنترلی کد ملی ایران"""
    if not code or not re.match(r'^\d{10}$', code.strip()):
        return False
    code = code.strip()
    if len(set(code)) == 1:
        return False
    checksum = int(code[9])
    s = sum(int(code[i]) * (10 - i) for i in range(9))
    remainder = s % 11
    return (remainder < 2 and checksum == remainder) or (remainder >= 2 and checksum == 11 - remainder)


def is_safe_url(target: str) -> bool:
    """جلوگیری از حملات Open Redirect"""
    if not target:
        return False
    ref_url = urlsplit(request.host_url)
    test_url = urlsplit(target)
    if test_url.scheme in ('http', 'https') and ref_url.netloc != test_url.netloc:
        return False
    if target.startswith('//') or target.startswith('\\'):
        return False
    return True


def save_secure_file(file_storage, subfolder: str, allowed_extensions: set = None) -> str:
    """آپلود ایمن: جلوگیری از Web Shell، Path Traversal و بازنویسی فایل‌ها"""
    if not file_storage or not file_storage.filename:
        return None

    if allowed_extensions is None:
        allowed_extensions = current_app.config.get('ALLOWED_EXTENSIONS', {'png', 'jpg', 'jpeg', 'webp', 'pdf'})

    orig_name = secure_filename(file_storage.filename)
    if '.' not in orig_name:
        raise ValueError("فرمت فایل نامعتبر است.")

    ext = orig_name.rsplit('.', 1)[1].lower()
    if ext not in allowed_extensions:
        raise ValueError(f"پسوند .{ext} مجاز نمی‌باشد.")

    unique_filename = f"{uuid.uuid4().hex}.{ext}"
    upload_dir = os.path.join(current_app.root_path, 'static', 'uploads', subfolder)
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, unique_filename)

    file_storage.save(file_path)
    return unique_filename


def delete_file_safely(subfolder: str, filename: str, default_files: set = None):
    """حذف فیزیکی فایل‌های بدون استفاده از سرور با مدیریت استثنا"""
    if not filename:
        return
    if default_files and filename in default_files:
        return
    file_path = os.path.join(current_app.root_path, 'static', 'uploads', subfolder, filename)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        try:
            os.remove(file_path)
        except OSError:
            pass


def admin_required(f):
    """دکوراتور حفاظت از مسیرهای پنل مدیریت"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function