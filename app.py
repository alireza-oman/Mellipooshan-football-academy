import os
from flask import Flask, render_template
from extensions import db, login_manager, migrate, csrf, limiter
from config import config_by_name
from models import (User, AboutUsMain, AboutFeature, AboutFacility,
                    Coach, AboutAgeGroup, Achievement, AboutStat, GalleryItem)

def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'dev')

    app = Flask(__name__)
    app.config.from_object(config_by_name.get(config_name, config_by_name['default']))

    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    login_manager.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    @app.after_request
    def apply_security_headers(response):
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        # در سرور HTTPS فعال شود:
        # response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        return response

    # ثبت بلblueprintها
    from auth import auth_bp
    from panel import panel_bp
    from admin import admin_bp
    from enrollment import enrollment_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(panel_bp, url_prefix='/panel')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(enrollment_bp, url_prefix='/enrollment')

    # روت‌های عمومی
    @app.route('/')
    def home():
        about_main = AboutUsMain.query.first()
        return render_template('home.html', about_main=about_main)

    @app.route('/about')
    def about():
        about_main = AboutUsMain.query.first()
        features = AboutFeature.query.all()
        facilities = AboutFacility.query.all()
        coaches = Coach.query.all()
        age_groups = AboutAgeGroup.query.all()
        achievements = Achievement.query.all()
        stats = AboutStat.query.all()
        gallery = GalleryItem.query.all()

        return render_template(
            'about.html',
            about_main=about_main,
            features=features,
            facilities=facilities,
            coaches=coaches,
            age_groups=age_groups,
            achievements=achievements,
            stats=stats,
            gallery=gallery
        )

    # مدیریت خطاهای استاندارد
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('error/400.html'), 400

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('error/403.html'), 403

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('error/404.html'), 404

    @app.errorhandler(413)
    def file_too_large(e):
        return render_template('error/413.html', message="حجم فایل ارسالی بیش از حد مجاز است."), 413

    @app.errorhandler(429)
    def ratelimit_handler(e):
        return render_template('error/429.html', message="تعداد درخواست‌های شما بیش از حد مجاز است."), 429

    @app.errorhandler(500)
    def internal_server_error(e):
        db.session.rollback()
        return render_template('error/500.html'), 500

    # دستورات خط فرمان امن برای Flask CLI
    register_cli_commands(app)

    with app.app_context():
        db.create_all()

    return app


def register_cli_commands(app):
    import click
    from seed import run_seed

    @app.cli.command("seed")
    def seed_cmd():
        """داده‌های پیش‌فرض را در دیتابیس می‌ریزد."""
        run_seed()
        click.echo("Database seeded successfully.")

    @app.cli.command("create-admin")
    @click.argument("phone")
    @click.argument("password")
    def create_admin_cmd(phone, password):
        """ایجاد کاربر مدیر ارشد با اعتبارسنجی امن"""
        from security_utils import validate_iran_phone
        if not validate_iran_phone(phone):
            click.echo("Error: Invalid Iran phone number.")
            return

        existing = User.query.filter_by(phone=phone).first()
        if existing:
            click.echo("Error: User already exists.")
            return

        admin = User(
            first_name="مدیر",
            last_name="سیستم",
            phone=phone,
            is_admin=True
        )
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()
        click.echo(f"Admin user {phone} created successfully.")


app = create_app()

if __name__ == '__main__':
    # در پروداکشن باید با WSGI Server مثل Gunicorn یا uWSGI اجرا شود
    app.run(host='127.0.0.1', port=5000)