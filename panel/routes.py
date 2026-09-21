from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from extensions import db
from models import Announcement, ClubRegistration, Training
from .forms import ProfileForm, AvatarForm, PasswordForm, SelectTrainingForm
from . import panel_bp
from security_utils import save_secure_file, delete_file_safely

@panel_bp.route('/dashboard')
@login_required
def dashboard():
    user_registrations = ClubRegistration.query.filter_by(user_id=current_user.id).all()
    latest_announcements = Announcement.query.order_by(Announcement.created_at.desc()).limit(5).all()
    return render_template('panel/dashboard.html',
                           registrations=user_registrations,
                           announcements=latest_announcements)


@panel_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    profile_form = ProfileForm(prefix='profile')
    avatar_form = AvatarForm(prefix='avatar')
    password_form = PasswordForm(prefix='password')

    if request.method == 'GET':
        profile_form.first_name.data = current_user.first_name
        profile_form.last_name.data = current_user.last_name

    # تفکیک دقیق فرم‌ها بدون ایجاد تداخل در اعتبارسنجی
    if profile_form.submit_profile.data and profile_form.validate_on_submit():
        current_user.first_name = profile_form.first_name.data.strip()
        current_user.last_name = profile_form.last_name.data.strip()
        db.session.commit()
        flash('اطلاعات کاربری شما به‌روزرسانی شد.', 'success')
        return redirect(url_for('panel.profile'))

    if avatar_form.submit_avatar.data and avatar_form.validate_on_submit():
        try:
            new_avatar = save_secure_file(avatar_form.avatar.data, 'avatars')
            if new_avatar:
                old_avatar = current_user.avatar
                current_user.avatar = new_avatar
                db.session.commit()
                delete_file_safely('avatars', old_avatar, default_files={'default-avatar.png'})
                flash('تصویر پروفایل شما با موفقیت تغییر کرد.', 'success')
                return redirect(url_for('panel.profile'))
        except Exception as e:
            db.session.rollback()
            flash(f'خطا در ذخیره تصویر: {e}', 'danger')

    if password_form.submit_password.data and password_form.validate_on_submit():
        if current_user.check_password(password_form.current_password.data):
            current_user.set_password(password_form.new_password.data)
            db.session.commit()
            flash('رمز عبور شما با موفقیت تغییر یافت.', 'success')
            return redirect(url_for('panel.profile'))
        else:
            flash('رمز عبور فعلی نادرست است.', 'danger')

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

    # دفاع در برابر IDOR
    if reg.user_id != current_user.id:
        abort(403)

    if reg.payment_status != 'paid':
        flash('برای انتخاب جلسه تمرینی، ابتدا باید وضعیت شهریه شما تایید شده باشد.', 'danger')
        return redirect(url_for('panel.dashboard'))

    all_trainings = Training.query.order_by(Training.created_at.desc()).all()
    form = SelectTrainingForm()
    form.training_id.choices = [(t.id, f"{t.title} ({t.days} - {t.time})") for t in all_trainings]

    if request.method == 'GET' and reg.training_id:
        form.training_id.data = reg.training_id

    if form.validate_on_submit():
        # بررسی صحت وجود جلسه تمرین در دیتابیس
        selected_training = Training.query.get(form.training_id.data)
        if not selected_training:
            flash('شیفت تمرینی انتخاب‌شده نامعتبر است.', 'danger')
        else:
            reg.training_id = selected_training.id
            db.session.commit()
            flash(f'شیفت تمرینی بازیکن «{reg.player_fullname}» ثبت شد.', 'success')
            return redirect(url_for('panel.dashboard'))

    return render_template('panel/select_trainings.html',
                           reg=reg,
                           form=form,
                           all_trainings=all_trainings)