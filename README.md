# ⚽ سامانه جامع مدیریت و ثبت‌نام آکادمی فوتبال ملی‌پوشان

یک وب‌اپلیکیشن یکپارچه و مدرن برای مدارس و آکادمی‌های فوتبال پایه، ساخته‌شده با **Flask (Python)**، پایگاه‌داده **SQLAlchemy** و طراحی کاملاً راست‌چین و ریسپانسیو (RTL).

## 🌟 ویژگی‌های کلیدی پروژه

### 👨‍👩‍👦 پنل اولیا و بازیکنان

* **ثبت‌نام چندمرحله‌ای (Multi-Step Form):** فرم ۶ مرحله‌ای هوشمند همراه با دراپ‌زون اختصاصی برای آپلود مدارک:

  * عکس پرسنلی
  * شناسنامه
  * بیمه ورزشی
  * رضایت‌نامه
* **رهگیری پرونده:** بررسی وضعیت مدارک و مشاهده دلایل رد احتمالی توسط مدیریت.
* **پرداخت شهریه و انتخاب شیفت:** امکان انتخاب شیفت تمرینی ثابت هفتگی پس از تأیید شهریه.
* **پروفایل کاربری:** مدیریت مشخصات، تغییر رمز عبور و آپلود آواتار با پیش‌نمایش زنده.

### 👑 پنل مدیریت ارشد (Admin Dashboard)

* **بررسی پرونده‌های ثبت‌نام:** مشاهده مشخصات کامل، پیش‌نمایش اسناد و تأیید یا رد مدارک همراه با ثبت علت.
* **مدیریت پرداخت‌ها:** بررسی درخواست‌های شهریه و تأیید یا لغو آن‌ها.
* **برنامه‌ریزی شیفت‌های تمرینی:** تعریف، ویرایش و حذف جلسات تمرینی رده‌های مختلف سنی.
* **سیستم اطلاعیه‌رسانی:** انتشار اطلاعیه‌ها در دسته‌بندی‌های مختلف با قابلیت تعیین میزان فوریت.
* **مدیریت پویای محتوا (CMS):** مدیریت بخش‌های مختلف صفحه «درباره ما»، مربیان، افتخارات، آمارها و گالری تصاویر.
* **مدیریت کاربران:** مشاهده، تغییر سطح دسترسی و حذف اعضا با قابلیت صفحه‌بندی (Pagination).

## 🛠️ تکنولوژی‌های استفاده‌شده

### Backend

* Python 3
* Flask
* Flask-SQLAlchemy
* Flask-Login
* Flask-WTF
* Flask-Migrate

### Database

* SQLite
* سازگار با PostgreSQL و MySQL

### Frontend

* HTML5
* CSS3
* Vanilla JavaScript
* Jinja2
* FontAwesome 6

### Fonts

* Vazirmatn
* Teko

## 🚀 راهنمای نصب و راه‌اندازی محلی

### 1. کلون کردن مخزن

```bash
git clone https://github.com/your-username/football-academy.git
cd football-academy
```

### 2. ساخت و فعال‌سازی محیط مجازی

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. نصب وابستگی‌ها

```bash
pip install -r requirements.txt
```

### 4. آماده‌سازی دیتابیس و داده‌های اولیه

```bash
python seed.py
```

### 5. اجرای پروژه

```bash
python app.py
```

سپس مرورگر خود را باز کرده و وارد آدرس زیر شوید:

```text
http://127.0.0.1:5000
```

## 👤 حساب کاربری مدیر پیش‌فرض

پس از اجرای پروژه، یک کاربر مدیر با دسترسی ادمین به‌صورت پیش‌فرض ایجاد می‌شود.

* **شماره موبایل:** `---`

> در صورت استفاده از پروژه در محیط واقعی، حتماً اطلاعات ورود پیش‌فرض را تغییر دهید.

## 📂 ساختار پروژه

```text
football-academy/
│
├── admin/                    # بلوپرینت و منطق پنل مدیریت
├── auth/                     # بلوپرینت احراز هویت
├── enrollment/               # ثبت‌نام دوره‌ها و آپلود اسناد
├── panel/                    # پنل کاربری بازیکنان
│
├── static/
│   ├── css/                 # استایل‌های عمومی و پنل‌ها
│   ├── js/                  # اسکریپت‌های تعاملی
│   └── uploads/             # تصاویر و مدارک آپلودشده
│
├── templates/               # قالب‌های Jinja2
│
├── app.py                   # نقطه ورود اصلی برنامه
├── config.py                # تنظیمات Development و Production
├── extensions.py            # نمونه‌سازی Extensionهای Flask
├── models.py                # مدل‌های پایگاه داده
├── seed.py                  # ایجاد داده‌های اولیه
├── requirements.txt         # وابستگی‌های Python
├── .gitignore               # فایل‌های نادیده گرفته‌شده توسط Git
└── README.md                # مستندات پروژه
```

## 📌 ارسال پروژه به GitHub

اگر هنوز Repository را به Git متصل نکرده‌اید:

```bash
git init
git add .
git commit -m "Initial commit: Football Academy Management System"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
git push -u origin main
```

برای تغییرات بعدی:

```bash
git add .
git commit -m "Update project"
git push
```

## 🔐 نکات امنیتی

قبل از انتشار پروژه در GitHub، اطلاعات حساس را داخل کد قرار ندهید.

مواردی مانند:

* `SECRET_KEY`
* رمز عبور مدیر
* اطلاعات اتصال به دیتابیس
* API Keyها
* اطلاعات درگاه پرداخت

باید در Environment Variables یا فایل‌های محلی قرار بگیرند و در `.gitignore` ثبت شوند.

## 📄 License

این پروژه تحت مجوز **MIT License** منتشر شده است.

## 🏷️ Tags

`Python` `Flask` `SQLAlchemy` `Flask-Login` `Flask-WTF` `Flask-Migrate` `SQLite` `JavaScript` `HTML5` `CSS3` `Jinja2` `Football Academy` `Management System` `RTL` `Web Application`
