from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed

class AnnouncementForm(FlaskForm):
    title = StringField('عنوان اطلاعیه', validators=[
        DataRequired(message="وارد کردن عنوان الزامی است."),
        Length(max=200, message="عنوان نباید بیشتر از ۲۰۰ کاراکتر باشد.")
    ])

    content = TextAreaField('متن اطلاعیه', validators=[
        DataRequired(message="وارد کردن متن اطلاعیه الزامی است.")
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

    is_important = BooleanField('علامت‌گذاری به عنوان فوری / مهم')

    submit = SubmitField('انتشار اطلاعیه در باشگاه')


class AdminUserEditForm(FlaskForm):
    first_name = StringField('نام', validators=[DataRequired(message="وارد کردن نام الزامی است.")])
    last_name = StringField('نام خانوادگی', validators=[DataRequired(message="وارد کردن نام خانوادگی الزامی است.")])

    phone = StringField('شماره موبایل', validators=[
        DataRequired(message="شماره موبایل الزامی است."),
        Length(min=11, max=11, message="شماره موبایل باید ۱۱ رقم باشد.")
    ])

    is_admin = BooleanField('دسترسی مدیریت (ادمین)')
    submit = SubmitField('ثبت تغییرات کاربر')


class EmptyForm(FlaskForm):
    pass


class RejectRegistrationForm(FlaskForm):
    reject_reason = StringField('علت رد پرونده یا نقص مدارک', validators=[
        DataRequired(message="وارد کردن علت رد یا نقص مدارک الزامی است.")
    ])
    submit_reject = SubmitField('ثبت علت و رد پرونده')


class AboutMainForm(FlaskForm):
    established_year = StringField('سال تأسیس آکادمی', validators=[DataRequired(message="این فیلد الزامی است.")])
    main_goal = TextAreaField('هدف اصلی آکادمی', validators=[DataRequired(message="این فیلد الزامی است.")])
    age_summary = StringField('خلاصه رده‌های سنی فعال', validators=[DataRequired(message="این فیلد الزامی است.")])
    intro_image = FileField('تصویر معرفی اصلی', validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], 'فقط فرمت‌های تصویر JPG و PNG مجاز هستند.')
    ])

    mission = TextAreaField('مأموریت آکادمی', validators=[DataRequired(message="این فیلد الزامی است.")])
    vision = TextAreaField('چشم‌انداز آینده', validators=[DataRequired(message="این فیلد الزامی است.")])
    long_term_goals = TextAreaField('اهداف بلندمدت', validators=[DataRequired(message="این فیلد الزامی است.")])

    cta_title = StringField('عنوان کادر ثبت‌نام', validators=[DataRequired(message="این فیلد الزامی است.")])
    cta_text = TextAreaField('متن کادر ثبت‌نام', validators=[DataRequired(message="این فیلد الزامی است.")])
    cta_btn_text = StringField('متن دکمه ثبت‌نام', validators=[DataRequired(message="این فیلد الزامی است.")])

    submit = SubmitField('ذخیره و به‌روزرسانی اطلاعات اصلی')


class AboutFeatureForm(FlaskForm):
    title = StringField('عنوان ویژگی (مثلاً: مربیان مجرب)', validators=[DataRequired(message="عنوان الزامی است.")])
    description = TextAreaField('توضیح کوتاه ویژگی', validators=[DataRequired(message="توضیح الزامی است.")])
    icon = SelectField('انتخاب آیکون', choices=[
        ('award', '🏆 مدال / افتخار'),
        ('users', '👥 مربیان / تیم'),
        ('shield', '🛡️ محیط امن / ایمنی'),
        ('check-circle', '✅ کیفیت / استاندارد'),
        ('target', '🎯 هدف / رشد علمی'),
        ('heart', '❤️ اخلاق و رشد فردی')
    ], default='check-circle')
    submit = SubmitField('ذخیره ویژگی')


class AboutFacilityForm(FlaskForm):
    title = StringField('عنوان امکانات (مثلاً: زمین چمن طبیعی)', validators=[DataRequired(message="عنوان الزامی است.")])
    description = TextAreaField('توضیحات امکانات', validators=[DataRequired(message="توضیح الزامی است.")])
    image = FileField('تصویر امکانات', validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], 'فقط فرمت‌های تصویر مجاز هستند.')
    ])
    submit = SubmitField('ذخیره امکانات')


class CoachForm(FlaskForm):
    name = StringField('نام و نام خانوادگی مربی', validators=[DataRequired(message="نام الزامی است.")])
    role = StringField('سمت و مدرک مربیگری (مثلاً: سرمربی / مدرک A آسیا)', validators=[DataRequired(message="سمت الزامی است.")])
    bio = TextAreaField('سوابق و بیوگرافی کوتاه')
    photo = FileField('عکس مربی', validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], 'فقط فرمت‌های تصویر مجاز هستند.')
    ])
    submit = SubmitField('ذخیره مربی')


class AboutAgeGroupForm(FlaskForm):
    title = StringField('عنوان رده سنی (مثلاً: نونهالان)', validators=[DataRequired(message="عنوان الزامی است.")])
    age_range = StringField('محدوده سنی (مثلاً: ۱۰ تا ۱۳ سال)', validators=[DataRequired(message="محدوده سنی الزامی است.")])
    description = TextAreaField('توضیحات برنامه تمرینی این رده')
    submit = SubmitField('ذخیره رده سنی')


class AchievementForm(FlaskForm):
    title = StringField('عنوان افتخار (مثلاً: قهرمانی لیگ استان)', validators=[DataRequired(message="عنوان الزامی است.")])
    year = StringField('سال کسب افتخار (مثلاً: ۱۴۰۲)', validators=[DataRequired(message="سال الزامی است.")])
    description = TextAreaField('توضیحات تکمیلی')
    submit = SubmitField('ذخیره افتخار')


class AboutStatForm(FlaskForm):
    number = StringField('عدد آمار (مثلاً: ۲۰۰+)', validators=[DataRequired(message="عدد الزامی است.")])
    label = StringField('عنوان آمار (مثلاً: بازیکن فعال)', validators=[DataRequired(message="عنوان الزامی است.")])
    icon = SelectField('انتخاب آیکون', choices=[
        ('users', '👥 بازیکنان'),
        ('user-check', '👨‍🏫 مربیان'),
        ('calendar', '📅 سال فعالیت'),
        ('trophy', '🏆 مسابقات / کاپ')
    ], default='users')
    submit = SubmitField('ذخیره آمار')


class GalleryItemForm(FlaskForm):
    title = StringField('عنوان تصویر (اختیاری)')
    image = FileField('فایل تصویر', validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], 'فقط تصاویر مجاز هستند.')
    ])
    category = SelectField('دسته‌بندی تصویر', choices=[
        ('تمرینات', 'تمرینات'),
        ('مسابقات', 'مسابقات'),
        ('مراسم‌ها', 'مراسم‌ها و جوایز')
    ], default='تمرینات')
    submit = SubmitField('آپلود در گالری')


class TrainingForm(FlaskForm):
    title = StringField('عنوان شیفت / گروه تمرینی (مثلاً: نونهالان - شیفت عصر)', validators=[
        DataRequired(message="عنوان تمرین الزامی است.")
    ])
    age_group = StringField('رده سنی (مثلاً: ۱۰ تا ۱۳ سال)', validators=[
        DataRequired(message="وارد کردن رده سنی الزامی است.")
    ])
    days = StringField('روزهای برگزاری (مثلاً: روزهای زوج)', validators=[
        DataRequired(message="روزهای برگزاری الزامی است.")
    ])
    time = StringField('ساعت برگزاری (مثلاً: ۱۶:۳۰ الی ۱۸:۰۰)', validators=[
        DataRequired(message="ساعت برگزاری الزامی است.")
    ])
    venue_name = StringField('محل برگزاری (مثلاً: زمین چمن شماره ۱ آزادی)', validators=[
        DataRequired(message="محل برگزاری الزامی است.")
    ])
    coach_name = StringField('نام مربی مسئول (اختیاری)')
    notes = TextAreaField('توضیحات یا نکات مهم (اختیاری)')

    submit = SubmitField('ثبت برنامه تمرین')