from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError, \
    Optional, Regexp
from flask_wtf.file import FileField, FileAllowed, FileRequired
from models import ClubRegistration

PHONE_REGEX = r'^09\d{9}$'
PHONE_ERROR_MSG = "شماره موبایل نامعتبر است. شماره باید با 09 شروع شده و ۱۱ رقم انگلیسی باشد."


class ClubRegistrationForm(FlaskForm):
    player_fullname = StringField('نام و نام خانوادگی بازیکن', validators=[
        DataRequired(message="وارد کردن نام و نام خانوادگی بازیکن الزامی است.")
    ])

    birth_date = StringField('تاریخ تولد بازیکن (شمسی)', validators=[
        DataRequired(message="وارد کردن تاریخ تولد الزامی است.")
    ])

    national_id = StringField('کد ملی بازیکن', validators=[
        DataRequired(message="وارد کردن کد ملی الزامی است."),
        Length(min=10, max=10, message="کد ملی باید دقیقاً ۱۰ رقم باشد.")
    ])

    player_phone = StringField('شماره موبایل', validators=[
        DataRequired(message="شماره موبایل الزامی است."),
        Regexp(PHONE_REGEX, message=PHONE_ERROR_MSG)
    ])

    parent_fullname = StringField('نام و نام خانوادگی ولی', validators=[
        DataRequired(message="وارد کردن نام و نام خانوادگی ولی الزامی است.")
    ])

    parent_relation = SelectField('نسبت با بازیکن', choices=[
        ('پدر', 'پدر'),
        ('مادر', 'مادر'),
        ('سایر', 'سایر (قیم قانونی)')
    ], validators=[DataRequired(message="انتخاب نسبت الزامی است.")])

    parent_phone = StringField('شماره موبایل', validators=[
        DataRequired(message="شماره موبایل الزامی است."),
        Regexp(PHONE_REGEX, message=PHONE_ERROR_MSG)
    ])

    province = StringField('استان', validators=[
        DataRequired(message="وارد کردن استان الزامی است.")
    ])

    city = StringField('شهر', validators=[
        DataRequired(message="وارد کردن شهر الزامی است.")
    ])

    address = TextAreaField('آدرس دقیق محل سکونت', validators=[
        DataRequired(message="وارد کردن آدرس الزامی است.")
    ])

    postal_code = StringField('کد پستی (اختیاری)', validators=[Optional()])

    football_history = TextAreaField('سابقه فوتبال (اختیاری)', validators=[Optional()])

    play_position = StringField('پست بازی مورد علاقه (اختیاری)', validators=[Optional()])

    player_photo = FileField('عکس پرسنلی بازیکن', validators=[
        FileRequired(message="آپلود عکس پرسنلی بازیکن الزامی است."),
        FileAllowed(['jpg', 'jpeg', 'png'], 'فقط تصاویر با فرمت JPG یا PNG مجاز هستند.')
    ])

    birth_cert_img = FileField('تصویر شناسنامه بازیکن', validators=[
        FileRequired(message="آپلود تصویر شناسنامه الزامی است."),
        FileAllowed(['jpg', 'jpeg', 'png'], 'فقط تصاویر با فرمت JPG یا PNG مجاز هستند.')
    ])

    parent_consent_img = FileField('رضایت‌نامه ولی', validators=[
        FileRequired(message="آپلود تصویر رضایت‌نامه ولی الزامی است."),
        FileAllowed(['jpg', 'jpeg', 'png'], 'فقط تصاویر با فرمت JPG یا PNG مجاز هستند.')
    ])

    medical_cert_img = FileField('گواهی سلامت پزشکی', validators=[
        FileRequired(message="آپلود تصویر گواهی سلامت پزشکی الزامی است."),
        FileAllowed(['jpg', 'jpeg', 'png'], 'فقط تصاویر با فرمت JPG یا PNG مجاز هستند.')
    ])

    sports_insurance_img = FileField('کارت بیمه ورزشی', validators=[
        FileRequired(message="آپلود تصویر کارت بیمه ورزشی الزامی است."),
        FileAllowed(['jpg', 'jpeg', 'png'], 'فقط تصاویر با فرمت JPG یا PNG مجاز هستند.')
    ])

    medical_notes = TextAreaField('توضیحات بیماری، شکستگی، مصرف دارو و... (اختیاری)', validators=[Optional()])

    submit = SubmitField('ثبت نهایی اطلاعات و ارسال مدارک')

    def validate_national_id(self, national_id):
        existing_reg = ClubRegistration.query.filter_by(national_id=national_id.data).first()
        if existing_reg:
            raise ValidationError('این کد ملی قبلاً ثبت‌نام شده است.')