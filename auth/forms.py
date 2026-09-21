from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, Regexp

PHONE_REGEX = r'^09\d{9}$'
PHONE_ERROR_MSG = "شماره موبایل نامعتبر است (باید ۱۱ رقم بوده و با 09 شروع شود)."

class SignupForm(FlaskForm):
    first_name = StringField('نام', validators=[
        DataRequired(message="وارد کردن نام الزامی است."),
        Length(min=2, max=50, message="نام باید بین ۲ تا ۵۰ کاراکتر باشد.")
    ])
    last_name = StringField('نام خانوادگی', validators=[
        DataRequired(message="وارد کردن نام خانوادگی الزامی است."),
        Length(min=2, max=50, message="نام خانوادگی باید بین ۲ تا ۵۰ کاراکتر باشد.")
    ])
    phone = StringField('شماره موبایل', validators=[
        DataRequired(message="شماره موبایل الزامی است."),
        Regexp(PHONE_REGEX, message=PHONE_ERROR_MSG)
    ])
    password = PasswordField('رمز عبور', validators=[
        DataRequired(message="رمز عبور الزامی است."),
        Length(min=8, max=64, message="رمز عبور باید حداقل ۸ کاراکتر باشد.")
    ])
    confirm_password = PasswordField('تکرار رمز عبور', validators=[
        DataRequired(message="تکرار رمز عبور الزامی است."),
        EqualTo('password', message="رمز عبور و تکرار آن یکسان نیستند.")
    ])
    submit = SubmitField('ثبت‌نام در آکادمی')


class LoginForm(FlaskForm):
    phone = StringField('شماره موبایل', validators=[
        DataRequired(message="شماره موبایل الزامی است."),
        Regexp(PHONE_REGEX, message=PHONE_ERROR_MSG)
    ])
    password = PasswordField('رمز عبور', validators=[
        DataRequired(message="رمز عبور الزامی است.")
    ])
    remember = BooleanField('مرا به خاطر بسپار')
    submit = SubmitField('ورود به سیستم')