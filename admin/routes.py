from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from . import admin_bp
from .forms import (AnnouncementForm, AdminUserEditForm, EmptyForm, RejectRegistrationForm, AboutMainForm,
                    AboutFeatureForm, AboutFacilityForm, CoachForm, AboutAgeGroupForm, AchievementForm, AboutStatForm,
                    GalleryItemForm, TrainingForm)
from models import (Announcement, User, ClubRegistration, AboutUsMain, AboutFeature, AboutFacility, Coach,
                    AboutAgeGroup, Achievement, AboutStat, GalleryItem, Training)
from extensions import db
from security_utils import admin_required, save_secure_file, delete_file_safely

@admin_bp.route('/')
@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    return render_template(
        'admin/dashboard.html',
        total_users=User.query.count(),
        total_announcements=Announcement.query.count(),
        total_registrations=ClubRegistration.query.count(),
        pending_registrations=ClubRegistration.query.filter_by(status='pending_approval').count()
    )

# --- اطلاعیه‌ها ---
@admin_bp.route('/announcements')
@login_required
@admin_required
def announcements_list():
    return render_template(
        'admin/announcements_list.html',
        announcements=Announcement.query.order_by(Announcement.created_at.desc()).all(),
        empty_form=EmptyForm()
    )

@admin_bp.route('/announcements/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_announcement():
    form = AnnouncementForm()
    if form.validate_on_submit():
        ann = Announcement(
            title=form.title.data.strip(),
            content=form.content.data.strip(),
            category=form.category.data,
            author=form.author.data.strip(),
            is_important=form.is_important.data
        )
        db.session.add(ann)
        db.session.commit()
        flash('اطلاعیه جدید با موفقیت منتشر شد.', 'success')
        return redirect(url_for('admin.announcements_list'))
    return render_template('admin/add_announcement.html', form=form)

@admin_bp.route('/announcements/edit/<int:ann_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_announcement(ann_id):
    announcement = Announcement.query.get_or_404(ann_id)
    form = AnnouncementForm(obj=announcement)
    if form.validate_on_submit():
        announcement.title = form.title.data.strip()
        announcement.content = form.content.data.strip()
        announcement.category = form.category.data
        announcement.author = form.author.data.strip()
        announcement.is_important = form.is_important.data
        db.session.commit()
        flash('اطلاعیه با موفقیت ویرایش شد.', 'success')
        return redirect(url_for('admin.announcements_list'))
    return render_template('admin/edit_announcement.html', form=form, announcement=announcement)

@admin_bp.route('/announcements/delete/<int:ann_id>', methods=['POST'])
@login_required
@admin_required
def delete_announcement(ann_id):
    form = EmptyForm()
    if form.validate_on_submit():
        announcement = Announcement.query.get_or_404(ann_id)
        db.session.delete(announcement)
        db.session.commit()
        flash('اطلاعیه حذف شد.', 'success')
    else:
        flash('خطای امنیتی CSRF در درخواست حذف.', 'danger')
    return redirect(url_for('admin.announcements_list'))

# --- مدیریت کاربران ---
@admin_bp.route('/users')
@login_required
@admin_required
def users_list():
    page = request.args.get('page', 1, type=int)
    pagination = db.paginate(User.query.order_by(User.created_at.desc()), page=page, per_page=15, error_out=False)
    return render_template('admin/users.html', users=pagination.items, pagination=pagination, form=EmptyForm())

@admin_bp.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = AdminUserEditForm(obj=user)
    if form.validate_on_submit():
        clean_phone = form.phone.data.strip()
        if clean_phone != user.phone:
            if User.query.filter_by(phone=clean_phone).first():
                flash('این شماره موبایل قبلاً توسط کاربر دیگری ثبت شده است.', 'danger')
                return render_template('admin/edit_user.html', form=form, user=user)

        user.first_name = form.first_name.data.strip()
        user.last_name = form.last_name.data.strip()
        user.phone = clean_phone
        user.is_active = form.is_active.data

        # ادمین نمی‌تواند دسترسی ادمینی خودش را سلب کند
        if user.id != current_user.id:
            user.is_admin = form.is_admin.data

        db.session.commit()
        flash(f'اطلاعات کاربر {user.full_name} به‌روزرسانی شد.', 'success')
        return redirect(url_for('admin.users_list'))
    return render_template('admin/edit_user.html', form=form, user=user)

@admin_bp.route('/users/delete/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    if user_id == current_user.id:
        flash('شما نمی‌توانید حساب مدیریت خودتان را حذف کنید!', 'danger')
        return redirect(url_for('admin.users_list'))

    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.get_or_404(user_id)
        if user.is_admin and User.query.filter_by(is_admin=True).count() <= 1:
            flash('امکان حذف تنها ادمین باقی‌مانده سیستم وجود ندارد!', 'danger')
            return redirect(url_for('admin.users_list'))

        delete_file_safely('avatars', user.avatar, default_files={'default-avatar.png'})
        db.session.delete(user)
        db.session.commit()
        flash(f'کاربر {user.full_name} حذف شد.', 'success')
    else:
        flash('درخواست حذف فاقد اعتبار است.', 'danger')
    return redirect(url_for('admin.users_list'))

# --- ثبت‌نام‌ها و پرونده‌ها ---
@admin_bp.route('/registrations')
@login_required
@admin_required
def registrations_list():
    return render_template('admin/registrations_list.html',
                           registrations=ClubRegistration.query.order_by(ClubRegistration.created_at.desc()).all(),
                           empty_form=EmptyForm())

@admin_bp.route('/registrations/view/<int:reg_id>')
@login_required
@admin_required
def view_registration(reg_id):
    return render_template('admin/view_registration.html',
                           reg=ClubRegistration.query.get_or_404(reg_id),
                           empty_form=EmptyForm(),
                           reject_form=RejectRegistrationForm())

@admin_bp.route('/registrations/approve/<int:reg_id>', methods=['POST'])
@login_required
@admin_required
def approve_registration(reg_id):
    form = EmptyForm()
    if form.validate_on_submit():
        reg = ClubRegistration.query.get_or_404(reg_id)
        reg.status = 'approved'
        reg.reject_reason = None
        db.session.commit()
        flash(f'پرونده بازیکن "{reg.player_fullname}" با موفقیت تایید شد.', 'success')
    return redirect(url_for('admin.view_registration', reg_id=reg_id))

@admin_bp.route('/registrations/reject/<int:reg_id>', methods=['POST'])
@login_required
@admin_required
def reject_registration(reg_id):
    form = RejectRegistrationForm()
    if form.validate_on_submit():
        reg = ClubRegistration.query.get_or_404(reg_id)
        reg.status = 'rejected'
        reg.reject_reason = form.reject_reason.data.strip()
        db.session.commit()
        flash(f'پرونده بازیکن "{reg.player_fullname}" رد شد.', 'info')
    else:
        flash('لطفاً دلیل رد پرونده را مشخص کنید.', 'danger')
    return redirect(url_for('admin.view_registration', reg_id=reg_id))

# --- شهریه‌ها و امور مالی ---
@admin_bp.route('/payments')
@login_required
@admin_required
def payments_list():
    regs = ClubRegistration.query.filter(ClubRegistration.payment_status != 'unpaid').order_by(ClubRegistration.created_at.desc()).all()
    return render_template('admin/payments_list.html', registrations=regs, empty_form=EmptyForm())

@admin_bp.route('/payments/approve/<int:payment_id>', methods=['POST'])
@login_required
@admin_required
def approve_payment(payment_id):
    form = EmptyForm()
    if form.validate_on_submit():
        reg = ClubRegistration.query.get_or_404(payment_id)
        reg.payment_status = 'paid'
        db.session.commit()
        flash(f'پرداخت بازیکن "{reg.player_fullname}" تایید شد.', 'success')
    return redirect(url_for('admin.payments_list'))

@admin_bp.route('/payments/reject/<int:payment_id>', methods=['POST'])
@login_required
@admin_required
def reject_payment(payment_id):
    form = EmptyForm()
    if form.validate_on_submit():
        reg = ClubRegistration.query.get_or_404(payment_id)
        reg.payment_status = 'rejected'
        db.session.commit()
        flash(f'پرداخت بازیکن "{reg.player_fullname}" رد شد.', 'info')
    return redirect(url_for('admin.payments_list'))

# --- شیفت‌های تمرینی ---
@admin_bp.route('/trainings')
@login_required
@admin_required
def trainings_list():
    return render_template('admin/trainings.html',
                           trainings=Training.query.order_by(Training.created_at.desc()).all(),
                           form=TrainingForm(),
                           empty_form=EmptyForm())

@admin_bp.route('/add_training', methods=['POST'])
@login_required
@admin_required
def add_training():
    form = TrainingForm()
    if form.validate_on_submit():
        new_training = Training(
            title=form.title.data.strip(),
            age_group=form.age_group.data.strip(),
            days=form.days.data.strip(),
            time=form.time.data.strip(),
            venue_name=form.venue_name.data.strip(),
            address=form.address.data.strip(),
            coach_name=form.coach_name.data.strip() if form.coach_name.data else None,
            notes=form.notes.data.strip() if form.notes.data else None
        )
        db.session.add(new_training)
        db.session.commit()
        flash('شیفت تمرینی جدید با موفقیت ثبت شد.', 'success')
    else:
        flash('خطا در ثبت اطلاعات تمرین. فیلدهای الزامی را پر کنید.', 'danger')
    return redirect(url_for('admin.trainings_list'))

@admin_bp.route('/trainings/delete/<int:training_id>', methods=['POST'])
@login_required
@admin_required
def delete_training(training_id):
    form = EmptyForm()
    if form.validate_on_submit():
        training = Training.query.get_or_404(training_id)
        db.session.delete(training)
        db.session.commit()
        flash('شیفت تمرینی حذف شد.', 'info')
    return redirect(url_for('admin.trainings_list'))

# --- مدیریت صفحه درباره ما و رسانه‌ها (همراه با پاکسازی فایل‌ها) ---
@admin_bp.route('/about')
@login_required
@admin_required
def manage_about():
    about_main = AboutUsMain.query.first()
    return render_template(
        'admin/about.html',
        about_main=about_main,
        main_form=AboutMainForm(obj=about_main) if about_main else AboutMainForm(),
        feature_form=AboutFeatureForm(),
        facility_form=AboutFacilityForm(),
        coach_form=CoachForm(),
        age_form=AboutAgeGroupForm(),
        achievement_form=AchievementForm(),
        stat_form=AboutStatForm(),
        gallery_form=GalleryItemForm(),
        empty_form=EmptyForm(),
        features=AboutFeature.query.all(),
        facilities=AboutFacility.query.all(),
        coaches=Coach.query.all(),
        age_groups=AboutAgeGroup.query.all(),
        achievements=Achievement.query.all(),
        stats=AboutStat.query.all(),
        gallery=GalleryItem.query.all()
    )

@admin_bp.route('/about/main/save', methods=['POST'])
@login_required
@admin_required
def save_about_main():
    about_main = AboutUsMain.query.first()
    if not about_main:
        about_main = AboutUsMain()
        db.session.add(about_main)

    form = AboutMainForm()
    if form.validate_on_submit():
        about_main.established_year = form.established_year.data
        about_main.main_goal = form.main_goal.data
        about_main.age_summary = form.age_summary.data
        about_main.mission = form.mission.data
        about_main.vision = form.vision.data
        about_main.long_term_goals = form.long_term_goals.data
        about_main.cta_title = form.cta_title.data
        about_main.cta_text = form.cta_text.data
        about_main.cta_btn_text = form.cta_btn_text.data

        if form.intro_image.data and form.intro_image.data.filename:
            old_img = about_main.intro_image
            new_img = save_secure_file(form.intro_image.data, 'about')
            if new_img:
                about_main.intro_image = new_img
                delete_file_safely('about', old_img, default_files={'about-intro-default.jpg'})

        db.session.commit()
        flash('اطلاعات با موفقیت ذخیره شدند.', 'success')
    return redirect(url_for('admin.manage_about'))

@admin_bp.route('/about/facility/add', methods=['POST'])
@login_required
@admin_required
def add_about_facility():
    form = AboutFacilityForm()
    if form.validate_on_submit():
        img = save_secure_file(form.image.data, 'about') or 'facility-default.jpg'
        facility = AboutFacility(title=form.title.data.strip(), description=form.description.data.strip(), image=img)
        db.session.add(facility)
        db.session.commit()
        flash('امکانات جدید افزوده شد.', 'success')
    return redirect(url_for('admin.manage_about') + '#tab-facilities')

@admin_bp.route('/about/facility/delete/<int:item_id>', methods=['POST'])
@login_required
@admin_required
def delete_about_facility(item_id):
    form = EmptyForm()
    if form.validate_on_submit():
        facility = AboutFacility.query.get_or_404(item_id)
        delete_file_safely('about', facility.image, default_files={'facility-default.jpg'})
        db.session.delete(facility)
        db.session.commit()
        flash('امکانات حذف شد.', 'info')
    return redirect(url_for('admin.manage_about') + '#tab-facilities')

@admin_bp.route('/about/coach/add', methods=['POST'])
@login_required
@admin_required
def add_coach():
    form = CoachForm()
    if form.validate_on_submit():
        photo = save_secure_file(form.photo.data, 'coaches') or 'coach-default.jpg'
        coach = Coach(name=form.name.data.strip(), role=form.role.data.strip(), bio=form.bio.data, photo=photo)
        db.session.add(coach)
        db.session.commit()
        flash('مربی جدید ذخیره شد.', 'success')
    return redirect(url_for('admin.manage_about') + '#tab-coaches')

@admin_bp.route('/about/coach/delete/<int:item_id>', methods=['POST'])
@login_required
@admin_required
def delete_coach(item_id):
    form = EmptyForm()
    if form.validate_on_submit():
        coach = Coach.query.get_or_404(item_id)
        delete_file_safely('coaches', coach.photo, default_files={'coach-default.jpg'})
        db.session.delete(coach)
        db.session.commit()
        flash('مربی حذف شد.', 'info')
    return redirect(url_for('admin.manage_about') + '#tab-coaches')

@admin_bp.route('/about/gallery/add', methods=['POST'])
@login_required
@admin_required
def add_gallery_item():
    form = GalleryItemForm()
    if form.validate_on_submit():
        img = save_secure_file(form.image.data, 'gallery')
        if img:
            item = GalleryItem(title=form.title.data, category=form.category.data, image=img)
            db.session.add(item)
            db.session.commit()
            flash('تصویر با موفقیت آپلود شد.', 'success')
        else:
            flash('لطفاً یک تصویر انتخاب کنید.', 'warning')
    return redirect(url_for('admin.manage_about') + '#tab-gallery')

@admin_bp.route('/about/gallery/delete/<int:item_id>', methods=['POST'])
@login_required
@admin_required
def delete_gallery_item(item_id):
    form = EmptyForm()
    if form.validate_on_submit():
        gallery = GalleryItem.query.get_or_404(item_id)
        delete_file_safely('gallery', gallery.image)
        db.session.delete(gallery)
        db.session.commit()
        flash('تصویر از گالری حذف شد.', 'info')
    return redirect(url_for('admin.manage_about') + '#tab-gallery')

@admin_bp.route('/about/feature/add', methods=['POST'])
@login_required
@admin_required
def add_about_feature():
    form = AboutFeatureForm()
    if form.validate_on_submit():
        db.session.add(AboutFeature(title=form.title.data, description=form.description.data, icon=form.icon.data))
        db.session.commit()
        flash('ویژگی ذخیره شد.', 'success')
    return redirect(url_for('admin.manage_about') + '#tab-features')

@admin_bp.route('/about/feature/delete/<int:item_id>', methods=['POST'])
@login_required
@admin_required
def delete_about_feature(item_id):
    form = EmptyForm()
    if form.validate_on_submit():
        feature = AboutFeature.query.get_or_404(item_id)
        db.session.delete(feature)
        db.session.commit()
        flash('ویژگی حذف شد.', 'info')
    return redirect(url_for('admin.manage_about') + '#tab-features')

@admin_bp.route('/about/age/add', methods=['POST'])
@login_required
@admin_required
def add_about_age():
    form = AboutAgeGroupForm()
    if form.validate_on_submit():
        db.session.add(AboutAgeGroup(title=form.title.data, age_range=form.age_range.data, description=form.description.data))
        db.session.commit()
        flash('رده سنی افزوده شد.', 'success')
    return redirect(url_for('admin.manage_about') + '#tab-ages')

@admin_bp.route('/about/age/delete/<int:item_id>', methods=['POST'])
@login_required
@admin_required
def delete_about_age(item_id):
    form = EmptyForm()
    if form.validate_on_submit():
        age = AboutAgeGroup.query.get_or_404(item_id)
        db.session.delete(age)
        db.session.commit()
        flash('رده سنی حذف شد.', 'info')
    return redirect(url_for('admin.manage_about') + '#tab-ages')

@admin_bp.route('/about/achievement/add', methods=['POST'])
@login_required
@admin_required
def add_achievement():
    form = AchievementForm()
    if form.validate_on_submit():
        db.session.add(Achievement(title=form.title.data, year=form.year.data, description=form.description.data))
        db.session.commit()
        flash('افتخار افزوده شد.', 'success')
    return redirect(url_for('admin.manage_about') + '#tab-achievements')

@admin_bp.route('/about/achievement/delete/<int:item_id>', methods=['POST'])
@login_required
@admin_required
def delete_achievement(item_id):
    form = EmptyForm()
    if form.validate_on_submit():
        ach = Achievement.query.get_or_404(item_id)
        db.session.delete(ach)
        db.session.commit()
        flash('افتخار حذف شد.', 'info')
    return redirect(url_for('admin.manage_about') + '#tab-achievements')

@admin_bp.route('/about/stat/add', methods=['POST'])
@login_required
@admin_required
def add_about_stat():
    form = AboutStatForm()
    if form.validate_on_submit():
        db.session.add(AboutStat(number=form.number.data, label=form.label.data, icon=form.icon.data))
        db.session.commit()
        flash('آمار افزوده شد.', 'success')
    return redirect(url_for('admin.manage_about') + '#tab-stats')

@admin_bp.route('/about/stat/delete/<int:item_id>', methods=['POST'])
@login_required
@admin_required
def delete_about_stat(item_id):
    form = EmptyForm()
    if form.validate_on_submit():
        st = AboutStat.query.get_or_404(item_id)
        db.session.delete(st)
        db.session.commit()
        flash('آمار حذف شد.', 'info')
    return redirect(url_for('admin.manage_about') + '#tab-stats')