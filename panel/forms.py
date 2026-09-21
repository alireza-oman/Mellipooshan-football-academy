from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo
from flask_wtf.file import FileField, FileAllowed, FileRequired

class ProfileForm(FlaskForm):
    first_name = StringField('نام', validators=[
        DataRequired(message="وارد کردن نام الزامی است."),
        Length(min=2, max=50)
    ])
    last_name = StringField('نام خانوادگی', validators=[
        DataRequired(message="وارد کردن نام خانوادگی الزامی است."),
        Length(min=2, max=50)
    ])
    submit_profile = SubmitField('ذخیره اطلاعات')


class AvatarForm(FlaskForm):
    avatar = FileField('تصویر پروفایل', validators=[
        FileRequired(message="لطفاً تصویری انتخاب کنید."),
        FileAllowed(['jpg', 'jpeg', 'png', 'webp'], 'فرمت‌های مجاز: JPG, PNG, WEBP')
    ])
    submit_avatar = SubmitField('بروزرسانی تصویر')


class PasswordForm(FlaskForm):
    current_password = PasswordField('رمز عبور فعلی', validators=[
        DataRequired(message="وارد کردن رمز عبور فعلی الزامی است.")
    ])
    new_password = PasswordField('رمز عبور جدید', validators=[
        DataRequired(message="وارد کردن رمز عبور جدید الزامی است."),
        Length(min=8, max=64, message="رمز عبور جدید باید حداقل ۸ کاراکتر باشد.")
    ])
    confirm_password = PasswordField('تکرار رمز عبور جدید', validators=[
        DataRequired(message="تکرار رمز عبور جدید الزامی است."),
        EqualTo('new_password', message="رمز عبور جدید و تکرار آن یکسان نیستند.")
    ])
    submit_password = SubmitField('تغییر رمز عبور')


class SelectTrainingForm(FlaskForm):
    training_id = SelectField('انتخاب شیفت تمرینی', coerce=int, validators=[DataRequired(message="شیفت تمرینی را انتخاب نمایید.")])
    submit_training = SubmitField('ثبت نهایی تمرین')