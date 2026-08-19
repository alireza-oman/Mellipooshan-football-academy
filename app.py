import os
from flask import Flask, render_template
from extensions import db, login_manager, migrate
from models import (User, AboutUsMain, AboutFeature, AboutFacility, Coach,
AboutAgeGroup, Achievement, AboutStat, GalleryItem)
from config import config_by_name
from auth import auth_bp
from panel import panel_bp
from admin import admin_bp
from enrollment import enrollment_bp

app = Flask(__name__)

env = os.environ.get('FLASK_ENV', 'dev')
app.config.from_object(config_by_name[env])

db.init_app(app)
login_manager.init_app(app)

migrate.init_app(app, db, render_as_batch=True)

app.register_blueprint(auth_bp)
app.register_blueprint(panel_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(enrollment_bp)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


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

    return render_template('about.html',
                           about_main=about_main,
                           features=features,
                           facilities=facilities,
                           coaches=coaches,
                           age_groups=age_groups,
                           achievements=achievements,
                           stats=stats,
                           gallery=gallery)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html'), 404


@app.errorhandler(403)
def forbidden(e):
    return render_template('error/403.html'), 403


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        user = User.query.filter_by(phone='09035619305').first()
        if user:
            user.is_admin = True
            db.session.commit()

    app.run(debug=True)





