import os
import uuid
from flask import render_template, redirect, url_for, flash, current_app, abort
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from . import enrollment_bp
from .forms import ClubRegistrationForm
from models import ClubRegistration
from extensions import db


def save_document(file_data):
    if not file_data:
        return None

    filename = secure_filename(file_data.filename)
    _, ext = os.path.splitext(filename)
    ext = ext.lower()

    random_filename = f"{uuid.uuid4().hex}{ext}"

    upload_dir = os.path.join(current_app.root_path, 'static', 'uploads', 'documents')
    os.makedirs(upload_dir, exist_ok=True)

    filepath = os.path.join(upload_dir, random_filename)
    file_data.save(filepath)

    return random_filename


@enrollment_bp.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    form = ClubRegistrationForm()

    if form.validate_on_submit():
        saved_files = []
        try:
            photo_fn = save_document(form.player_photo.data)
            saved_files.append(photo_fn)
            birth_cert_fn = save_document(form.birth_cert_img.data)
            saved_files.append(birth_cert_fn)
            consent_fn = save_document(form.parent_consent_img.data)
            saved_files.append(consent_fn)
            medical_fn = save_document(form.medical_cert_img.data)
            saved_files.append(medical_fn)
            insurance_fn = save_document(form.sports_insurance_img.data)
            saved_files.append(insurance_fn)

            new_registration = ClubRegistration(
                user_id=current_user.id,
                player_fullname=form.player_fullname.data,
                birth_date=form.birth_date.data,
                national_id=form.national_id.data,
                player_phone=form.player_phone.data,
                parent_fullname=form.parent_fullname.data,
                parent_relation=form.parent_relation.data,
                parent_phone=form.parent_phone.data,
                province=form.province.data,
                city=form.city.data,
                address=form.address.data,
                postal_code=form.postal_code.data or None,
                football_history=form.football_history.data or None,
                play_position=form.play_position.data or None,
                player_photo=photo_fn,
                birth_cert_img=birth_cert_fn,
                parent_consent_img=consent_fn,
                medical_cert_img=medical_fn,
                sports_insurance_img=insurance_fn,
                medical_notes=form.medical_notes.data or None
            )

            db.session.add(new_registration)
            db.session.commit()

            flash(f'درخواست ثبت‌نام بازیکن "{form.player_fullname.data}" با موفقیت ارسال شد.', 'success')
            return redirect(url_for('panel.dashboard'))

        except Exception as e:
            db.session.rollback()
            upload_dir = os.path.join(current_app.root_path, 'static', 'uploads', 'documents')
            for fn in saved_files:
                if fn:
                    fp = os.path.join(upload_dir, fn)
                    if os.path.exists(fp):
                        os.remove(fp)
            flash('خطایی در ثبت اطلاعات رخ داد. لطفاً مجدداً تلاش کنید.', 'danger')

    return render_template('enrollment/register_course.html', form=form)


@enrollment_bp.route('/pay/<int:reg_id>')
@login_required
def payment(reg_id):
    reg = ClubRegistration.query.get_or_404(reg_id)

    if reg.user_id != current_user.id:
        abort(403)

    reg.payment_status = 'pending_approval'
    db.session.commit()

    flash(f'پرداخت شهریه برای بازیکن "{reg.player_fullname}" با موفقیت ثبت شد و در انتظار تایید مدیریت قرار گرفت.', 'info')
    return redirect(url_for('panel.dashboard'))