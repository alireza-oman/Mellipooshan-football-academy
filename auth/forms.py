from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, Regexp

PHONE_REGEX = r'^09\d{9}$'
PHONE_ERROR_MSG = "شماره موبایل نامعتبر است. شماره باید با 09 شروع شده و ۱۱ رقم انگلیسی باشد."

class SignupForm(FlaskForm):
    first_name = StringField('نام', validators=[DataRequired(message="وارد کردن نام الزامی است.")])
    last_name = StringField('نام خانوادگی', validators=[DataRequired(message="وارد کردن نام خانوادگی الزامی است.")])
    phone = StringField('شماره موبایل', validators=[
        DataRequired(message="شماره موبایل الزامی است."),
        Regexp(PHONE_REGEX, message=PHONE_ERROR_MSG)
    ])
    password = PasswordField('رمز عبور', validators=[
        DataRequired(message="رمز عبور الزامی است."),
        Length(min=6, message="رمز عبور باید حداقل ۶ کاراکتر باشد.")
    ])
    confirm_password = PasswordField('تکرار رمز عبور', validators=[
        DataRequired(message="تکرار رمز عبور الزامی است."),
        EqualTo('password', message="رمز عبور و تکرار آن مطابقت ندارند.")
    ])
    submit = SubmitField('ثبت‌نام در سایت')


class LoginForm(FlaskForm):
    phone = StringField('شماره موبایل', validators=[
        DataRequired(message="شماره موبایل الزامی است."),
        Length(min=11, max=11, message="شماره موبایل باید ۱۱ رقم باشد.")
    ])
    password = PasswordField('رمز عبور', validators=[
        DataRequired(message="رمز عبور الزامی است.")
    ])
    remember = BooleanField('مرا به خاطر بسپار')
    submit = SubmitField('ورود به حساب کاربری')


