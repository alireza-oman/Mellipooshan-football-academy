from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from extensions import db
from sqlalchemy import event
from sqlalchemy.engine import Engine

# فعال کردن Foreign Keys فقط برای SQLite
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if dbapi_connection.__class__.__module__.startswith("sqlite3"):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    avatar = db.Column(db.String(255), nullable=False, default='default-avatar.png')
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    club_registrations = db.relationship(
        'ClubRegistration',
        backref='user',
        lazy='select',
        cascade="all, delete-orphan"
    )

    def set_password(self, password: str):
        if not password or len(password) < 8:
            raise ValueError("رمز عبور باید حداقل ۸ کاراکتر باشد.")
        # استفاده از متد scrypt برای امنیت بالاتر در برابر GPU Cracking
        self.password_hash = generate_password_hash(password, method='scrypt')

    def check_password(self, password: str) -> bool:
        if not self.password_hash or not password:
            return False
        return check_password_hash(self.password_hash, password)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Announcement(db.Model):
    __tablename__ = 'announcements'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False, default='عمومی')
    author = db.Column(db.String(100), nullable=False, default='مدیریت آکادمی')
    is_important = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), index=True, nullable=False)


class AgeGroup(db.Model):
    __tablename__ = 'age_groups'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    min_age = db.Column(db.Integer, nullable=False)
    max_age = db.Column(db.Integer, nullable=False)


class Training(db.Model):
    __tablename__ = 'trainings'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    venue_name = db.Column(db.String(150), nullable=False)
    address = db.Column(db.Text, nullable=False)
    equipment = db.Column(db.String(200), nullable=True)
    time = db.Column(db.String(50), nullable=False)
    days = db.Column(db.String(100), nullable=False)

    coach_name = db.Column(db.String(100), nullable=True)
    contact_phone = db.Column(db.String(15), nullable=True)
    notes = db.Column(db.Text, nullable=True)

    age_group_id = db.Column(db.Integer, db.ForeignKey('age_groups.id', ondelete='RESTRICT'), nullable=True, index=True)
    age_group = db.relationship('AgeGroup', backref='trainings')

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class ClubRegistration(db.Model):
    __tablename__ = 'club_registrations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)

    player_fullname = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.String(10), nullable=False)
    national_id = db.Column(db.String(10), unique=True, nullable=False, index=True)
    player_phone = db.Column(db.String(15), nullable=False)

    parent_fullname = db.Column(db.String(100), nullable=False)
    parent_relation = db.Column(db.String(20), nullable=False)
    parent_phone = db.Column(db.String(15), nullable=False)

    province = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    address = db.Column(db.Text, nullable=False)
    postal_code = db.Column(db.String(10), nullable=True)

    football_history = db.Column(db.Text, nullable=True)
    play_position = db.Column(db.String(50), nullable=True)

    player_photo = db.Column(db.String(255), nullable=False)
    birth_cert_img = db.Column(db.String(255), nullable=False)
    parent_consent_img = db.Column(db.String(255), nullable=False)
    medical_cert_img = db.Column(db.String(255), nullable=False)
    sports_insurance_img = db.Column(db.String(255), nullable=False)

    medical_notes = db.Column(db.Text, nullable=True)

    status = db.Column(db.String(30), default='pending_approval', nullable=False, index=True)
    reject_reason = db.Column(db.String(255), nullable=True)
    payment_status = db.Column(db.String(30), default='unpaid', nullable=False, index=True)

    training_id = db.Column(db.Integer, db.ForeignKey('trainings.id', ondelete='SET NULL'), nullable=True, index=True)
    training = db.relationship('Training', backref='registered_players')

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), index=True, nullable=False)


class AboutUsMain(db.Model):
    __tablename__ = 'about_us_main'

    id = db.Column(db.Integer, primary_key=True)
    established_year = db.Column(db.String(20), nullable=False)
    main_goal = db.Column(db.Text, nullable=False)
    age_summary = db.Column(db.String(100), nullable=False)
    intro_image = db.Column(db.String(255), default='about-intro-default.jpg')

    mission = db.Column(db.Text, nullable=False)
    vision = db.Column(db.Text, nullable=False)
    long_term_goals = db.Column(db.Text, nullable=False)

    cta_title = db.Column(db.String(200), nullable=False)
    cta_text = db.Column(db.Text, nullable=False)
    cta_btn_text = db.Column(db.String(50), nullable=False)


class AboutFeature(db.Model):
    __tablename__ = 'about_features'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    icon = db.Column(db.String(50), default='check-circle')


class AboutFacility(db.Model):
    __tablename__ = 'about_facilities'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(255), default='facility-default.jpg')


class Coach(db.Model):
    __tablename__ = 'coaches'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.Text, nullable=True)
    photo = db.Column(db.String(255), default='coach-default.jpg')


class AboutAgeGroup(db.Model):
    __tablename__ = 'about_age_groups'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    age_range = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)


class Achievement(db.Model):
    __tablename__ = 'achievements'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    year = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=True)


class AboutStat(db.Model):
    __tablename__ = 'about_stats'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(50), nullable=False)
    label = db.Column(db.String(100), nullable=False)
    icon = db.Column(db.String(50), default='users')


class GalleryItem(db.Model):
    __tablename__ = 'gallery_items'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=True)
    image = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(50), default='تمرینات')