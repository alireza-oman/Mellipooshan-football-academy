from app import app
from extensions import db
from models import AboutUsMain, AboutFeature, AboutAgeGroup, AboutStat
def seed_database():
    with app.app_context():
        main_about = AboutUsMain.query.first()

        if main_about:
            main_about.intro_image = 'about-intro-default.jpg'

        db.session.commit()

        if not AboutUsMain.query.first():
            main_about = AboutUsMain(
                established_year="۱۳۹۰",
                main_goal="پرورش استعدادهای برتر فوتبال پایه کشور",
                age_summary="رده‌های سنی ۶ تا ۱۸ سال",
                mission="آموزش علمی و اصولی فوتبال همراه با پرورش اخلاقی",
                vision="تبدیل شدن به برترین آکادمی تخصصی فوتبال پایه",
                long_term_goals="معرفی بازیکنان به تیم‌های مطرح کشور و تیم‌های ملی",
                cta_title="همین امروز مسیر حرفه‌ای شدن را شروع کن!",
                cta_text="برای شرکت در جلسات استعدادیابی و ثبت‌نام در آکادمی اقدام کنید.",
                cta_btn_text="ثبت‌نام در آکادمی"
            )
            db.session.add(main_about)

        if AboutFeature.query.count() == 0:
            db.session.add_all([
                AboutFeature(title="مربیان مجرب", description="بهره‌گیری از مربیان دارای مدرک A آسیا", icon="award"),
                AboutFeature(title="محیط امن", description="فضای استاندارد و امن برای رشد کودکان و نوجوانان", icon="shield")
            ])

        if AboutAgeGroup.query.count() == 0:
            db.session.add_all([
                AboutAgeGroup(title="خردسالان", age_range="۸ تا ۹ سال", description="آموزش مهارت‌های پایه و بازی‌محور"),
                AboutAgeGroup(title="نونهالان U14", age_range="۱۰ تا ۱۳ سال", description="آشنایی با تاکتیک‌های تیمی و مسابقات")
            ])

        if AboutStat.query.count() == 0:
            db.session.add_all([
                AboutStat(number="۲۰۰+", label="بازیکن فعال", icon="users"),
                AboutStat(number="۱۰+", label="سال سابقه", icon="calendar")
            ])

        db.session.commit()
        print("✅ داده‌های اولیه دیتابیس با موفقیت ثبت شدند (Database Seeded Successfully).")

if __name__ == '__main__':
    seed_database()