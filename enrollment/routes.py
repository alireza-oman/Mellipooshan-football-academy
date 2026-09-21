from flask import render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError
from . import enrollment_bp
from .forms import ClubRegistrationForm, PaySubmitForm
from models import ClubRegistration
from extensions import db
from security_utils import save_secure_file, delete_file_safely

@enrollment_bp.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    form = ClubRegistrationForm()

    if form.validate_on_submit():
        saved_files = []
        try:
            # ذخیره‌سازی فایل‌ها با اسم‌های امن غیرقابل دستکاری
            photo_fn = save_secure_file(form.player_photo.data, 'documents')
            saved_files.append(photo_fn)
            birth_fn = save_secure_file(form.birth_cert_img.data, 'documents')
            saved_files.append(birth_fn)
            consent_fn = save_secure_file(form.parent_consent_img.data, 'documents')
            saved_files.append(consent_fn)
            medical_fn = save_secure_file(form.medical_cert_img.data, 'documents')
            saved_files.append(medical_fn)
            insurance_fn = save_secure_file(form.sports_insurance_img.data, 'documents')
            saved_files.append(insurance_fn)

            new_registration = ClubRegistration(
                user_id=current_user.id,
                player_fullname=form.player_fullname.data.strip(),
                birth_date=form.birth_date.data.strip(),
                national_id=form.national_id.data.strip(),
                player_phone=form.player_phone.data.strip(),
                parent_fullname=form.parent_fullname.data.strip(),
                parent_relation=form.parent_relation.data,
                parent_phone=form.parent_phone.data.strip(),
                province=form.province.data.strip(),
                city=form.city.data.strip(),
                address=form.address.data.strip(),
                postal_code=form.postal_code.data.strip() if form.postal_code.data else None,
                football_history=form.football_history.data.strip() if form.football_history.data else None,
                play_position=form.play_position.data.strip() if form.play_position.data else None,
                player_photo=photo_fn,
                birth_cert_img=birth_fn,
                parent_consent_img=consent_fn,
                medical_cert_img=medical_fn,
                sports_insurance_img=insurance_fn,
                medical_notes=form.medical_notes.data.strip() if form.medical_notes.data else None
            )

            db.session.add(new_registration)
            db.session.commit()

            flash(f'درخواست ثبت‌نام بازیکن "{new_registration.player_fullname}" با موفقیت ارسال شد.', 'success')
            return redirect(url_for('panel.dashboard'))

        except IntegrityError:
            db.session.rollback()
            for fn in saved_files:
                delete_file_safely('documents', fn)
            flash('این کد ملی قبلاً در سیستم ثبت شده است.', 'danger')
        except Exception:
            db.session.rollback()
            # رول‌بک و پاکسازی فایل‌های آپلود شده در صورت بروز خطای دیتابیس
            for fn in saved_files:
                delete_file_safely('documents', fn)
            flash('خطا در ثبت اطلاعات. لطفاً فایل‌ها را بررسی کرده و مجدد اقدام فرمایید.', 'danger')

    return render_template('enrollment/register_course.html', form=form)


@enrollment_bp.route('/pay/<int:reg_id>', methods=['POST'])
@login_required
def payment(reg_id):
    """تغییر به POST جهت جلوگیری کامل از CSRF مالی"""
    form = PaySubmitForm()
    if not form.validate_on_submit():
        flash('درخواست پرداخت نامعتبر یا تاریخ مصرف گذشته است.', 'danger')
        return redirect(url_for('panel.dashboard'))

    reg = ClubRegistration.query.get_or_404(reg_id)

    # بررسی دسترسی مالکیت (جلوگیری از IDOR)
    if reg.user_id != current_user.id:
        abort(403)

    if reg.status != 'approved':
        flash('تنها پس از تایید مدارک توسط مدیریت، امکان پرداخت شهریه وجود دارد.', 'warning')
        return redirect(url_for('panel.dashboard'))

    reg.payment_status = 'pending_approval'
    db.session.commit()

    flash(f'پرداخت شهریه برای بازیکن "{reg.player_fullname}" ثبت شد و در انتظار تایید مدیریت است.', 'info')
    return redirect(url_for('panel.dashboard'))