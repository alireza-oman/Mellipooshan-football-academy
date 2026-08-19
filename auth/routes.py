from urllib.parse import urlsplit
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.exc import IntegrityError
from . import auth_bp
from .forms import SignupForm, LoginForm
from models import User
from extensions import db

@auth_bp.route('/signup', methods=['GET', 'POST'])
@auth_bp.route('/register', methods=['GET', 'POST'])
def signup():

    if current_user.is_authenticated:
        return redirect('/')

    form = SignupForm()

    if form.validate_on_submit():

        existing_user = User.query.filter_by(phone=form.phone.data).first()
        if existing_user:
            flash('این شماره موبایل قبلاً در سیستم ثبت شده است!', 'danger')
            return render_template('auth/signup.html', form=form)

        new_user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            phone=form.phone.data
        )

        new_user.set_password(form.password.data)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('ثبت‌نام با موفقیت انجام شد! حالا می‌توانید وارد شوید.', 'success')
            return redirect(url_for('auth.login'))

        except IntegrityError:
            db.session.rollback()
            flash('خطای سیستمی: این شماره موبایل در حال حاضر وجود دارد.', 'danger')

    return render_template('auth/signup.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(phone=form.phone.data).first()

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)

            next_page = request.args.get('next')
            if not next_page or urlsplit(next_page).netloc != '':
                next_page = '/'

            flash(f'خوش آمدید {user.first_name} جان!', 'success')
            return redirect(next_page)
        else:
            flash('شماره موبایل یا رمز عبور اشتباه است.', 'danger')

    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('با موفقیت از حساب کاربری خارج شدید.', 'info')
    return redirect('/')