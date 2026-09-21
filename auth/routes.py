from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.exc import IntegrityError
from . import auth_bp
from .forms import SignupForm, LoginForm
from models import User
from extensions import db, limiter
from security_utils import is_safe_url

@auth_bp.route('/signup', methods=['GET', 'POST'])
@auth_bp.route('/register', methods=['GET', 'POST'])
@limiter.limit("10 per hour")
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('panel.dashboard'))

    form = SignupForm()
    if form.validate_on_submit():
        clean_phone = form.phone.data.strip()
        existing_user = User.query.filter_by(phone=clean_phone).first()
        if existing_user:
            flash('این شماره موبایل قبلاً در سیستم ثبت شده است.', 'danger')
            return render_template('auth/signup.html', form=form)

        new_user = User(
            first_name=form.first_name.data.strip(),
            last_name=form.last_name.data.strip(),
            phone=clean_phone
        )
        try:
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash('ثبت‌نام شما با موفقیت انجام شد! اکنون می‌توانید وارد شوید.', 'success')
            return redirect(url_for('auth.login'))
        except IntegrityError:
            db.session.rollback()
            flash('این شماره موبایل پیش‌تر ثبت شده است.', 'danger')
        except Exception:
            db.session.rollback()
            flash('خطای سیستمی رخ داد. لطفاً مجدداً تلاش فرمایید.', 'danger')

    return render_template('auth/signup.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def login():
    if current_user.is_authenticated:
        return redirect(url_for('panel.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        clean_phone = form.phone.data.strip()
        user = User.query.filter_by(phone=clean_phone).first()

        if user and user.check_password(form.password.data):
            if not user.is_active:
                flash('حساب کاربری شما مسدود شده است. لطفاً با مدیریت تماس بگیرید.', 'danger')
                return render_template('auth/login.html', form=form)

            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if not next_page or not is_safe_url(next_page):
                next_page = url_for('panel.dashboard')

            flash(f'خوش آمدید، {user.first_name} عزیز!', 'success')
            return redirect(next_page)
        else:
            flash('شماره موبایل یا رمز عبور وارد شده نادرست است.', 'danger')

    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('با موفقیت از حساب کاربری خارج شدید.', 'info')
    return redirect(url_for('home'))