import uuid
from flask import render_template, redirect, url_for, flash, request, current_app, abort
from werkzeug.utils import secure_filename
import os

from extensions import db
from models import Announcement, ClubRegistration, Training
from .forms import ProfileForm, AvatarForm, PasswordForm
from panel import panel_bp
from flask_login import login_required, current_user


@panel_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('panel/dashboard.html')

@panel_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    profile_form = ProfileForm()
    avatar_form = AvatarForm()
    password_form = PasswordForm()

    if request.method == 'GET':
        profile_form.first_name.data = current_user.first_name
        profile_form.last_name.data = current_user.last_name

    if profile_form.submit_profile.data:
        if profile_form.validate_on_submit():
            current_user.first_name = profile_form.first_name.data
            current_user.last_name = profile_form.last_name.data

            db.session.commit()
            flash('اطلاعات کاربری شما با موفقیت به‌روزرسانی شد.', 'success')
            return redirect(url_for('panel.profile'))

    elif avatar_form.submit_avatar.data:
        if avatar_form.validate_on_submit():
            file = avatar_form.avatar.data
            filename = secure_filename(file.filename)
            _, ext = os.path.splitext(filename)
            ext = ext.lower()

            random_filename = f"{uuid.uuid4().hex}{ext}"
            upload_dir = os.path.join(current_app.root_path, 'static', 'uploads', 'avatars')
            os.makedirs(upload_dir, exist_ok=True)
            filepath = os.path.join(upload_dir, random_filename)

            old_avatar = current_user.avatar

            try:
                file.save(filepath)
                current_user.avatar = random_filename
                db.session.commit()

                if old_avatar and old_avatar != 'default-avatar.png':
                    old_filepath = os.path.join(upload_dir, old_avatar)
                    if os.path.exists(old_filepath):
                        os.remove(old_filepath)

                flash('تصویر پروفایل شما با موفقیت به‌روزرسانی شد.', 'success')
            except Exception:
                db.session.rollback()
                if os.path.exists(filepath):
                    os.remove(filepath)
                flash('خطا در ذخیره‌سازی تصویر.', 'danger')

            return redirect(url_for('panel.profile'))

    elif password_form.submit_password.data:
        if password_form.validate_on_submit():
            current_password = password_form.current_password.data
            new_password = password_form.new_password.data

            if current_user.check_password(current_password):
                current_user.set_password(new_password)
                db.session.commit()
                flash('رمز عبور شما با موفقیت تغییر یافت.', 'success')
                return redirect(url_for('panel.profile'))
            else:
                flash('رمز عبور فعلی وارد شده اشتباه است.', 'danger')

    return render_template('panel/profile.html',
                           profile_form=profile_form,
                           avatar_form=avatar_form,
                           password_form=password_form)

@panel_bp.route('/announcements')
@login_required
def announcements():
    all_announcements = Announcement.query.order_by(Announcement.created_at.desc()).all()
    return render_template('panel/announcements.html', announcements=all_announcements)


@panel_bp.route('/player/<int:reg_id>/trainings', methods=['GET', 'POST'])
@login_required
def select_trainings(reg_id):
    reg = ClubRegistration.query.get_or_404(reg_id)

    if reg.user_id != current_user.id:
        abort(403)

    if reg.payment_status != 'paid':
        flash('برای انتخاب جلسه تمرینی، ابتدا باید شهریه بازیکن تایید شده باشد.', 'danger')
        return redirect(url_for('panel.dashboard'))

    all_trainings = Training.query.order_by(Training.created_at.desc()).all()

    if request.method == 'POST':
        training_id = request.form.get('training_id', type=int)

        if training_id:
            reg.training_id = training_id
        else:
            reg.training_id = None

        db.session.commit()
        flash(f'شیفت تمرینی بازیکن «{reg.player_fullname}» با موفقیت ثبت شد.', 'success')
        return redirect(url_for('panel.dashboard'))

    return render_template('panel/select_trainings.html',
                           reg=reg,
                           all_trainings=all_trainings)