from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp, Optional
from flask_wtf.file import FileField, FileAllowed
from security_utils import PHONE_REGEX

class AnnouncementForm(FlaskForm):
    title = StringField('عنوان اطلاعیه', validators=[
        DataRequired(message="وارد کردن عنوان الزامی است."),
        Length(max=200, message="عنوان نباید بیشتر از ۲۰۰ کاراکتر باشد.")
    ])
    content = TextAreaField('متن اطلاعیه', validators=[
        DataRequired(message="وارد کردن متن الزامی است.")
    ])
    category = SelectField('دسته‌بندی', choices=[
        ('عمومی', 'عمومی'),
        ('تمرینات', 'تمرینات'),
        ('ثبت‌نام', 'ثبت‌نام'),
        ('اداری', 'اداری'),
        ('فوری', 'فوری')
    ], default='عمومی')
    author = StringField('نویسنده پیام', default='مدیریت آکادمی', validators=[
        DataRequired(message="نام نویسنده الزامی است.")
    ])
    is_important = BooleanField('فوری / مهم')
    submit = SubmitField('انتشار اطلاعیه')


class AdminUserEditForm(FlaskForm):
    first_name = StringField('نام', validators=[DataRequired(message="نام الزامی است.")])
    last_name = StringField('نام خانوادگی', validators=[DataRequired(message="نام خانوادگی الزامی است.")])
    phone = StringField('شماره موبایل', validators=[
        DataRequired(message="شماره موبایل الزامی است."),
        Regexp(PHONE_REGEX, message="فرمت موبایل صحیح نیست.")
    ])
    is_admin = BooleanField('دسترسی مدیریت (ادمین)')
    is_active = BooleanField('حساب کاربری فعال است')
    submit = SubmitField('ثبت تغییرات کاربر')


class EmptyForm(FlaskForm):
    """فرم امن توکن CSRF برای تمام دکمه‌های حذف و تغییر وضعیت سریع"""
    submit = SubmitField()


class RejectRegistrationForm(FlaskForm):
    reject_reason = StringField('علت رد پرونده یا نقص مدارک', validators=[
        DataRequired(message="ذکر علت الزامی است."),
        Length(min=3, max=255)
    ])
    submit_reject = SubmitField('ثبت علت و رد پرونده')


class AboutMainForm(FlaskForm):
    established_year = StringField('سال تأسیس', validators=[DataRequired()])
    main_goal = TextAreaField('هدف اصلی', validators=[DataRequired()])
    age_summary = StringField('خلاصه رده‌های سنی', validators=[DataRequired()])
    intro_image = FileField('تصویر معرفی اصلی', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'webp'], 'فرمت نامعتبر است.')
    ])
    mission = TextAreaField('مأموریت', validators=[DataRequired()])
    vision = TextAreaField('چشم‌انداز', validators=[DataRequired()])
    long_term_goals = TextAreaField('اهداف بلندمدت', validators=[DataRequired()])
    cta_title = StringField('عنوان کادر اقدام', validators=[DataRequired()])
    cta_text = TextAreaField('متن کادر اقدام', validators=[DataRequired()])
    cta_btn_text = StringField('متن دکمه', validators=[DataRequired()])
    submit = SubmitField('بروزرسانی درباره ما')


class AboutFeatureForm(FlaskForm):
    title = StringField('عنوان ویژگی', validators=[DataRequired()])
    description = TextAreaField('توضیح', validators=[DataRequired()])
    icon = SelectField('آیکون', choices=[
        ('award', '🏆 مدال'),
        ('users', '👥 مربیان'),
        ('shield', '🛡️ محیط امن'),
        ('check-circle', '✅ کیفیت'),
        ('target', '🎯 هدف'),
        ('heart', '❤️ رشد فردی')
    ], default='check-circle')
    submit = SubmitField('افزودن ویژگی')


class AboutFacilityForm(FlaskForm):
    title = StringField('عنوان امکانات', validators=[DataRequired()])
    description = TextAreaField('توضیحات', validators=[DataRequired()])
    image = FileField('تصویر امکانات', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'webp'], 'فرمت نامعتبر است.')
    ])
    submit = SubmitField('افزودن امکانات')


class CoachForm(FlaskForm):
    name = StringField('نام مربی', validators=[DataRequired()])
    role = StringField('سمت و مدرک', validators=[DataRequired()])
    bio = TextAreaField('سوابق')
    photo = FileField('عکس مربی', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'webp'], 'فرمت نامعتبر است.')
    ])
    submit = SubmitField('ذخیره مربی')


class AboutAgeGroupForm(FlaskForm):
    title = StringField('عنوان رده سنی', validators=[DataRequired()])
    age_range = StringField('محدوده سنی', validators=[DataRequired()])
    description = TextAreaField('توضیحات')
    submit = SubmitField('ذخیره رده سنی')


class AchievementForm(FlaskForm):
    title = StringField('عنوان افتخار', validators=[DataRequired()])
    year = StringField('سال کسب افتخار', validators=[DataRequired()])
    description = TextAreaField('توضیحات')
    submit = SubmitField('ذخیره افتخار')


class AboutStatForm(FlaskForm):
    number = StringField('عدد آمار', validators=[DataRequired()])
    label = StringField('عنوان آمار', validators=[DataRequired()])
    icon = SelectField('آیکون', choices=[
        ('users', '👥 بازیکنان'),
        ('user-check', '👨‍🏫 مربیان'),
        ('calendar', '📅 سابقه'),
        ('trophy', '🏆 کاپ')
    ], default='users')
    submit = SubmitField('ذخیره آمار')


class GalleryItemForm(FlaskForm):
    title = StringField('عنوان تصویر (اختیاری)', validators=[Optional(), Length(max=100)])
    image = FileField('فایل تصویر', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'webp'], 'فرمت نامعتبر است.')
    ])
    category = SelectField('دسته‌بندی', choices=[
        ('تمرینات', 'تمرینات'),
        ('مسابقات', 'مسابقات'),
        ('مراسم‌ها', 'مراسم‌ها و جوایز')
    ], default='تمرینات')
    submit = SubmitField('آپلود در گالری')


class TrainingForm(FlaskForm):
    title = StringField('عنوان شیفت تمرینی', validators=[DataRequired(message="عنوان الزامی است.")])
    age_group = StringField('رده سنی', validators=[DataRequired(message="رده سنی الزامی است.")])
    days = StringField('روزها', validators=[DataRequired(message="روزهای تمرین الزامی است.")])
    time = StringField('ساعت', validators=[DataRequired(message="ساعت برگزاری الزامی است.")])
    venue_name = StringField('نام زمین', validators=[DataRequired(message="نام محل تمرین الزامی است.")])
    address = TextAreaField('آدرس زمین', validators=[DataRequired(message="آدرس الزامی است.")])
    coach_name = StringField('نام مربی', validators=[Optional()])
    notes = TextAreaField('نکات تکمیلی', validators=[Optional()])
    submit = SubmitField('ثبت برنامه تمرین')