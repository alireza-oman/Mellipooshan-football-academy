import uuid

from flask import render_template, redirect, url_for, flash, abort, request, current_app
from flask_login import login_required, current_user
from functools import wraps

from werkzeug.utils import secure_filename

from . import admin_bp
from .forms import (AnnouncementForm, AdminUserEditForm, EmptyForm, RejectRegistrationForm, AboutMainForm,
                    AboutFeatureForm, AboutFacilityForm, CoachForm, AboutAgeGroupForm, AchievementForm, AboutStatForm,
                    GalleryItemForm, TrainingForm)
from models import (Announcement, User, ClubRegistration, AboutUsMain, AboutFeature, AboutFacility, Coach,
                    AboutAgeGroup, Achievement, AboutStat, GalleryItem, Training)
from extensions import db
import os


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)

    return decorated_function


def save_uploaded_file(file_data, folder_name):
    if not file_data or not file_data.filename:
        return None
    filename = secure_filename(file_data.filename)
    _, ext = os.path.splitext(filename)
    random_filename = f"{uuid.uuid4().hex}{ext.lower()}"
    upload_dir = os.path.join(current_app.root_path, 'static', 'uploads', folder_name)
    os.makedirs(upload_dir, exist_ok=True)
    filepath = os.path.join(upload_dir, random_filename)
    file_data.save(filepath)
    return random_filename

@admin_bp.route('/')
@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    total_users = User.query.count()
    total_announcements = Announcement.query.count()
    total_registrations = ClubRegistration.query.count()
    pending_registrations = ClubRegistration.query.filter_by(status='pending_approval').count()

    return render_template('admin/dashboard.html',
                           total_users=total_users,
                           total_announcements=total_announcements,
                           total_registrations=total_registrations,
                           pending_registrations=pending_registrations)


@admin_bp.route('/announcements')
@login_required
@admin_required
def announcements_list():
    all_announcements = Announcement.query.order_by(Announcement.created_at.desc()).all()
    empty_form = EmptyForm()

    return render_template('admin/announcements_list.html',
                           announcements=all_announcements,
                           empty_form=empty_form,
                           active_page='announcements_list')


@admin_bp.route('/announcements/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_announcement():
    form = AnnouncementForm()

    if form.validate_on_submit():
        ann = Announcement(
            title=form.title.data,
            content=form.content.data,
            category=form.category.data,
            author=form.author.data,
            is_important=form.is_important.data
        )

        db.session.add(ann)
        db.session.commit()

        flash('اطلاعیه جدید با موفقیت در باشگاه منتشر شد.', 'success')
        return redirect(url_for('admin.announcements_list'))

    return render_template('admin/add_announcement.html', form=form)


@admin_bp.route('/announcements/edit/<int:ann_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_announcement(ann_id):
    form = AnnouncementForm()

    announcement = Announcement.query.get_or_404(ann_id)

    if request.method == 'GET':
        form.title.data = announcement.title
        form.content.data = announcement.content
        form.category.data = announcement.category
        form.author.data = announcement.author
        form.is_important.data = announcement.is_important

    if form.validate_on_submit():
        announcement.title = form.title.data
        announcement.content = form.content.data
        announcement.category = form.category.data
        announcement.author = form.author.data
        announcement.is_important = form.is_important.data

        db.session.add(announcement)
        db.session.commit()

        flash('اطلاعیه مورد نظر با موفقیت ویرایش شد.', 'success')

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

        flash('اطلاعیه با موفقیت از سیستم حذف شد.', 'success')
    else:
        flash('درخواست حذف نامعتبر است.', 'danger')

    return redirect(url_for('admin.announcements_list'))


@admin_bp.route('/users')
@login_required
@admin_required
def users_list():
    page = request.args.get('page', 1, type=int)

    pagination = db.paginate(
        User.query.order_by(User.created_at.desc()),
        page=page,
        per_page=10,
        error_out=False
    )
    users = pagination.items
    form = EmptyForm()

    return render_template('admin/users.html', users=users, pagination=pagination, form=form)


@admin_bp.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = AdminUserEditForm()

    if request.method == 'GET':
        form.first_name.data = user.first_name
        form.last_name.data = user.last_name
        form.phone.data = user.phone
        form.is_admin.data = user.is_admin

    if form.validate_on_submit():
        if form.phone.data != user.phone:
            existing_user = User.query.filter_by(phone=form.phone.data).first()
            if existing_user:
                flash('این شماره موبایل قبلاً توسط کاربر دیگری ثبت شده است.', 'danger')
                return render_template('admin/edit_user.html', form=form, user=user)

        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.phone = form.phone.data


        if user.id != current_user.id:
            user.is_admin = form.is_admin.data

        db.session.commit()
        flash(f'اطلاعات کاربر {user.first_name} با موفقیت به‌روزرسانی شد.', 'success')
        return redirect(url_for('admin.users_list'))

    return render_template('admin/edit_user.html', form=form, user=user)


@admin_bp.route('/users/delete/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    if user_id == current_user.id:
        flash('شما نمی‌توانید حساب کاربری خودتان را حذف کنید!', 'danger')
        return redirect(url_for('admin.users_list'))

    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.get_or_404(user_id)

        if user.avatar and user.avatar != 'default-avatar.png':
            upload_dir = os.path.join(current_app.root_path, 'static', 'uploads', 'avatars')
            filepath = os.path.join(upload_dir, user.avatar)
            if os.path.exists(filepath):
                try:
                    os.remove(filepath)
                except OSError:
                    pass

        db.session.delete(user)
        db.session.commit()

        flash(f'کاربر {user.first_name} {user.last_name} با موفقیت حذف شد.', 'success')
    else:
        flash('درخواست حذف نامعتبر است (خطای امنیتی).', 'danger')

    return redirect(url_for('admin.users_list'))


@admin_bp.route('/registrations')
@login_required
@admin_required
def registrations_list():
    registrations = ClubRegistration.query.order_by(ClubRegistration.created_at.desc()).all()

    empty_form = EmptyForm()

    return render_template('admin/registrations_list.html',
                           registrations=registrations,
                           empty_form=empty_form,
                           active_page='registrations_list')


@admin_bp.route('/registrations/view/<int:reg_id>', methods=['GET'])
@login_required
@admin_required
def view_registration(reg_id):
    registration = ClubRegistration.query.get_or_404(reg_id)
    empty_form = EmptyForm()
    reject_form = RejectRegistrationForm()

    return render_template('admin/view_registration.html',
                           reg=registration,
                           empty_form=empty_form,
                           reject_form=reject_form)


@admin_bp.route('/registrations/approve/<int:reg_id>', methods=['POST'])
@login_required
@admin_required
def approve_registration(reg_id):
    form = EmptyForm()
    if form.validate_on_submit():
        registration = ClubRegistration.query.get_or_404(reg_id)

        registration.status = 'approved'
        registration.reject_reason = None
        db.session.commit()

        flash(f'پرونده ثبت‌نام بازیکن "{registration.player_fullname}" با موفقیت تایید شد.', 'success')
    else:
        flash('درخواست تایید نامعتبر است.', 'danger')

    return redirect(url_for('admin.view_registration', reg_id=reg_id))


@admin_bp.route('/registrations/reject/<int:reg_id>', methods=['POST'])
@login_required
@admin_required
def reject_registration(reg_id):
    form = RejectRegistrationForm()
    if form.validate_on_submit():
        registration = ClubRegistration.query.get_or_404(reg_id)

        registration.status = 'rejected'
        registration.reject_reason = form.reject_reason.data
        db.session.commit()

        flash(f'پرونده بازیکن "{registration.player_fullname}" به علت نقص مدارک رد شد.', 'info')
    else:
        flash('لطفاً فیلد علت رد پرونده را خالی نگذارید.', 'danger')

    return redirect(url_for('admin.view_registration', reg_id=reg_id))

@admin_bp.route('/about')
@login_required
@admin_required
def manage_about():
    about_main = AboutUsMain.query.first()

    main_form = AboutMainForm(obj=about_main) if about_main else AboutMainForm()
    feature_form = AboutFeatureForm()
    facility_form = AboutFacilityForm()
    coach_form = CoachForm()
    age_form = AboutAgeGroupForm()
    achievement_form = AchievementForm()
    stat_form = AboutStatForm()
    gallery_form = GalleryItemForm()
    empty_form = EmptyForm()

    return render_template('admin/about.html',
                           about_main=about_main,
                           main_form=main_form,
                           feature_form=feature_form,
                           facility_form=facility_form,
                           coach_form=coach_form,
                           age_form=age_form,
                           achievement_form=achievement_form,
                           stat_form=stat_form,
                           gallery_form=gallery_form,
                           empty_form=empty_form,
                           features=AboutFeature.query.all(),
                           facilities=AboutFacility.query.all(),
                           coaches=Coach.query.all(),
                           age_groups=AboutAgeGroup.query.all(),
                           achievements=Achievement.query.all(),
                           stats=AboutStat.query.all(),
                           gallery=GalleryItem.query.all())


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
            if about_main.intro_image and about_main.intro_image != 'about-intro-default.jpg':
                upload_dir = os.path.join(current_app.root_path, 'static', 'uploads', 'about')
                old_filepath = os.path.join(upload_dir, about_main.intro_image)
                if os.path.exists(old_filepath):
                    try:
                        os.remove(old_filepath)
                    except OSError:
                        pass

            new_image = save_uploaded_file(form.intro_image.data, 'about')
            if new_image:
                about_main.intro_image = new_image

        db.session.commit()
        flash('اطلاعات اصلی درباره ما با موفقیت به‌روزرسانی شد.', 'success')
    else:
        flash('خطا در ثبت اطلاعات. لطفاً تمام فیلدهای الزامی را پر کنید.', 'danger')

    return redirect(url_for('admin.manage_about'))


@admin_bp.route('/about/feature/add', methods=['POST'])
@login_required
@admin_required
def add_about_feature():
    feature_form = AboutFeatureForm()

    if feature_form.validate_on_submit():
        new_feature = AboutFeature(
            title=feature_form.title.data,
            description=feature_form.description.data,
            icon=feature_form.icon.data
        )
        db.session.add(new_feature)
        db.session.commit()
        flash('ویژگی جدید با موفقیت به بخش «چرا ما» اضافه شد.', 'success')
    else:
        flash('خطا در ثبت ویژگی. لطفاً فیلدهای الزامی را پر کنید.', 'danger')

    return redirect(url_for('admin.manage_about') + '#tab-features')


@admin_bp.route('/about/feature/delete/<int:item_id>', methods=['POST'])
@login_required
@admin_required
def delete_about_feature(item_id):
    feature = db.get_or_404(AboutFeature, item_id)
    db.session.delete(feature)
    db.session.commit()
    flash('ویژگی مورد نظر با موفقیت حذف شد.', 'info')
    return redirect(url_for('admin.manage_about') + '#tab-features')


@admin_bp.route('/about/facility/add', methods=['POST'])
@login_required
@admin_required
def add_about_facility():
    facility_form = AboutFacilityForm()

    if facility_form.validate_on_submit():
        image = save_uploaded_file(facility_form.image.data, 'about') or 'facility-default.jpg'

        new_facility = AboutFacility(
            title=facility_form.title.data,
            description=facility_form.description.data,
            image=image,
        )

        db.session.add(new_facility)
        db.session.commit()
        flash('امکانات جدید با موفقیت اضافه شد.', 'success')
    else:
        flash('خطا در ثبت امکانات. لطفاً فیلدهای الزامی را بررسی کنید.', 'danger')

    return redirect(url_for('admin.manage_about') + '#tab-facilities')


@admin_bp.route('/about/facility/delete/<int:item_id>', methods=['POST'])
@login_required
@admin_required
def delete_about_facility(item_id):
    facility = db.get_or_404(AboutFacility, item_id)
    db.session.delete(facility)
    db.session.commit()
    flash('امکانات مورد نظر با موفقیت حذف شد.', 'info')
    return redirect(url_for('admin.manage_about') + '#tab-facilities')


@admin_bp.route('/about/coach/add', methods=['POST'])
@login_required
@admin_required
def add_coach():
    coach_form = CoachForm()

    if coach_form.validate_on_submit():
        photo = save_uploaded_file(coach_form.photo.data, 'coaches') or 'coach-default.jpg'

        new_coach = Coach(
            name=coach_form.name.data,
            role=coach_form.role.data,
            bio=coach_form.bio.data,
            photo=photo,
        )

        db.session.add(new_coach)
        db.session.commit()
        flash('اطلاعات مربی جدید با موفقیت ذخیره شد.', 'success')
    else:
        flash('خطا در ثبت مربی. لطفاً فیلدهای الزامی را پر کنید.', 'danger')

    return redirect(url_for('admin.manage_about') + '#tab-coaches')


@admin_bp.route('/about/coach/delete/<int:item_id>', methods=['POST'])
@login_required
@admin_required
def delete_coach(item_id):
    coach = db.get_or_404(Coach, item_id)
    db.session.delete(coach)
    db.session.commit()
    flash('اطلاعات مربی با موفقیت حذف شد.', 'info')
    return redirect(url_for('admin.manage_about') + '#tab-coaches')


@admin_bp.route('/about/age/add', methods=['POST'])
@login_required
@admin_required
def add_about_age():
    age_form = AboutAgeGroupForm()
    if age_form.validate_on_submit():
        new_age = AboutAgeGroup(
            title=age_form.title.data,
            description=age_form.description.data,
            age_range=age_form.age_range.data,
        )
        db.session.add(new_age)
        db.session.commit()
        flash('رده سنی جدید با موفقیت اضافه شد.', 'success')
    else:
        flash('خطا در ثبت رده سنی. لطفاً تمامی فیلدها را پر کنید.', 'danger')

    return redirect(url_for('admin.manage_about') + '#tab-ages')


@admin_bp.route('/about/age/delete/<int:item_id>', methods=['POST'])
@login_required
@admin_required
def delete_about_age(item_id):
    age = db.get_or_404(AboutAgeGroup, item_id)
    db.session.delete(age)
    db.session.commit()
    flash('رده سنی مورد نظر با موفقیت حذف شد.', 'info')
    return redirect(url_for('admin.manage_about') + '#tab-ages')


@admin_bp.route('/about/achievement/add', methods=['POST'])
@login_required
@admin_required
def add_achievement():
    achievement_form = AchievementForm()
    if achievement_form.validate_on_submit():
        new_achievement = Achievement(
            title=achievement_form.title.data,
            description=achievement_form.description.data,
            year=achievement_form.year.data,
        )
        db.session.add(new_achievement)
        db.session.commit()
        flash('افتخار/دستاورد جدید با موفقیت ثبت شد.', 'success')
    else:
        flash('خطا در ثبت افتخار. لطفاً فیلدهای الزامی را بررسی کنید.', 'danger')

    return redirect(url_for('admin.manage_about') + '#tab-achievements')


@admin_bp.route('/about/achievement/delete/<int:item_id>', methods=['POST'])
@login_required
@admin_required
def delete_achievement(item_id):
    achievement = db.get_or_404(Achievement, item_id)
    db.session.delete(achievement)
    db.session.commit()
    flash('افتخار مورد نظر با موفقیت حذف شد.', 'info')
    return redirect(url_for('admin.manage_about') + '#tab-achievements')

@admin_bp.route('/about/stat/add', methods=['POST'])
@login_required
@admin_required
def add_about_stat():
    stat_form = AboutStatForm()
    if stat_form.validate_on_submit():
        new_stat = AboutStat(
            number=stat_form.number.data,
            label=stat_form.label.data,
            icon=stat_form.icon.data
        )
        db.session.add(new_stat)
        db.session.commit()
        flash('آمار جدید با موفقیت ثبت شد.', 'success')
    else:
        flash('خطا در ثبت آمار. لطفاً اطلاعات را بررسی کنید.', 'danger')

    return redirect(url_for('admin.manage_about') + '#tab-stats')


@admin_bp.route('/about/stat/delete/<int:item_id>', methods=['POST'])
@login_required
@admin_required
def delete_about_stat(item_id):
    stat = db.get_or_404(AboutStat, item_id)
    db.session.delete(stat)
    db.session.commit()
    flash('آمار مورد نظر با موفقیت حذف شد.', 'info')
    return redirect(url_for('admin.manage_about') + '#tab-stats')


@admin_bp.route('/about/gallery/add', methods=['POST'])
@login_required
@admin_required
def add_gallery_item():
    gallery_item_form = GalleryItemForm()
    if gallery_item_form.validate_on_submit():
        image = save_uploaded_file(gallery_item_form.image.data, 'gallery')
        if image:
            new_gallery_item = GalleryItem(
                title=gallery_item_form.title.data,
                category=gallery_item_form.category.data,
                image=image,
            )
            db.session.add(new_gallery_item)
            db.session.commit()
            flash('تصویر جدید با موفقیت به گالری اضافه شد.', 'success')
        else:
            flash('لطفاً یک تصویر برای آپلود انتخاب کنید.', 'danger')
    else:
        flash('خطا در آپلود تصویر گالری. فرم را بررسی کنید.', 'danger')

    return redirect(url_for('admin.manage_about') + '#tab-gallery')


@admin_bp.route('/about/gallery/delete/<int:item_id>', methods=['POST'])
@login_required
@admin_required
def delete_gallery_item(item_id):
    gallery_item = db.get_or_404(GalleryItem, item_id)

    if gallery_item.image:
        upload_dir = os.path.join(current_app.root_path, 'static', 'uploads', 'gallery')
        filepath = os.path.join(upload_dir, gallery_item.image)
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except OSError:
                pass

    db.session.delete(gallery_item)
    db.session.commit()
    flash('تصویر از گالری حذف شد.', 'info')
    return redirect(url_for('admin.manage_about') + '#tab-gallery')


@admin_bp.route('/payments')
@login_required
@admin_required
def payments_list():
    registrations = ClubRegistration.query.filter(ClubRegistration.payment_status != 'unpaid').order_by(ClubRegistration.created_at.desc()).all()
    empty_form = EmptyForm()
    return render_template('admin/payments_list.html',
                           registrations=registrations,
                           empty_form=empty_form,
                           active_page='payments')


@admin_bp.route('/payments/approve/<int:payment_id>', methods=['POST'])
@login_required
@admin_required
def approve_payment(payment_id):
    form = EmptyForm()
    if form.validate_on_submit():
        reg = ClubRegistration.query.get_or_404(payment_id)
        reg.payment_status = 'paid'
        db.session.commit()
        flash(f'پرداخت شهریه بازیکن "{reg.player_fullname}" با موفقیت تایید شد.', 'success')
    else:
        flash('درخواست نامعتبر است.', 'danger')
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
        flash(f'پرداخت شهریه بازیکن "{reg.player_fullname}" رد شد.', 'info')
    else:
        flash('درخواست نامعتبر است.', 'danger')
    return redirect(url_for('admin.payments_list'))


@admin_bp.route('/trainings')
@login_required
@admin_required
def trainings_list():
    trainings = Training.query.order_by(Training.created_at.desc()).all()
    form = TrainingForm()
    empty_form = EmptyForm()
    return render_template('admin/trainings.html',
                           trainings=trainings,
                           form=form,
                           empty_form=empty_form,
                           active_page='trainings')


@admin_bp.route('/add_training', methods=['POST'])
@login_required
@admin_required
def add_training():
    form = TrainingForm()

    if form.validate_on_submit():
        new_training = Training(
            title=form.title.data,
            age_group=form.age_group.data,
            days=form.days.data,
            time=form.time.data,
            venue_name=form.venue_name.data,
            address=form.venue_name.data,
            coach_name=form.coach_name.data or None,
            notes=form.notes.data or None
        )

        db.session.add(new_training)
        db.session.commit()
        flash('شیفت تمرینی جدید با موفقیت ثبت شد.', 'success')
    else:
        flash('خطا در ثبت تمرین. لطفاً فیلدهای الزامی را پر کنید.', 'danger')

    return redirect(url_for('admin.trainings_list'))


@admin_bp.route('/trainings/delete/<int:training_id>', methods=['POST'])
@login_required
@admin_required
def delete_training(training_id):
    form = EmptyForm()
    if form.validate_on_submit():
        training = db.get_or_404(Training, training_id)
        db.session.delete(training)
        db.session.commit()
        flash('برنامه تمرینی با موفقیت حذف شد.', 'info')
    else:
        flash('درخواست حذف نامعتبر است.', 'danger')

    return redirect(url_for('admin.trainings_list'))





