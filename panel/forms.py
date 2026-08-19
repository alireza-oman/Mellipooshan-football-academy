from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo
from flask_wtf.file import FileField, FileAllowed, FileRequired


class ProfileForm(FlaskForm):
    first_name = StringField('نام', validators=[DataRequired(message="وارد کردن نام الزامی است.")])
    last_name = StringField('نام خانوادگی', validators=[DataRequired(message="وارد کردن نام خانوادگی الزامی است.")])
    submit_profile = SubmitField('ذخیره اطلاعات کاربری')


class AvatarForm(FlaskForm):
    avatar = FileField('تصویر پروفایل', validators=[
        FileRequired(message="لطفاً ابتدا یک تصویر انتخاب کنید."),
        FileAllowed(['jpg', 'jpeg', 'png'], 'فقط تصاویر با فرمت JPG، JPEG یا PNG مجاز هستند.')
    ])
    submit_avatar = SubmitField('بروزرسانی تصویر')


class PasswordForm(FlaskForm):
    current_password = PasswordField('رمز عبور فعلی', validators=[
        DataRequired(message="وارد کردن رمز عبور فعلی الزامی است.")
    ])
    new_password = PasswordField('رمز عبور جدید', validators=[
        DataRequired(message="وارد کردن رمز عبور جدید الزامی است."),
        Length(min=6, message="رمز عبور جدید باید حداقل ۶ کاراکتر باشد.")
    ])
    confirm_password = PasswordField('تکرار رمز عبور جدید', validators=[
        DataRequired(message="تکرار رمز عبور جدید الزامی است."),
        EqualTo('new_password', message="رمز عبور جدید و تکرار آن مطابقت ندارند.")
    ])
    submit_password = SubmitField('تغییر رمز عبور')