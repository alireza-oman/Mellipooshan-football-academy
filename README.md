[English](#mellipooshan-football-academy) | [فارسی](#mellipooshan-football-academy-persian)

# Mellipooshan Football Academy

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-000000?logo=flask&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-D71F00?logo=sqlalchemy&logoColor=white)
![License](https://img.shields.io/badge/License-All%20Rights%20Reserved-lightgrey)

A modular, full-stack football academy management and online player registration platform built with **Python** and **Flask**. Designed with a responsive RTL interface for Persian-speaking users, it supports phone-based authentication, multi-step player registration with document uploads, tuition payment review, weekly training shift selection, announcements, and a dedicated administration panel with a built-in CMS.

---

## Features

- **User Authentication & Security:** Phone-based registration and login powered by `Flask-Login`, Werkzeug password hashing, remember-me sessions, safe redirect validation, CSRF protection (`Flask-WTF`), and rate limiting (`Flask-Limiter`).
- **Multi-Step Online Player Registration:** Guided 6-step enrollment form capturing player details, guardian information, football background, address, and required document uploads (personal photo, ID card, sports insurance, and consent form).
- **Player & Parent Panel:** Personal dashboard for tracking registration approval status (including rejection reasons), viewing payment status, selecting weekly training shifts after payment approval, reading academy announcements, and managing profile details, password, and avatar.
- **Administration Panel:** Role-protected management interface featuring live system statistics, paginated user management (with self-deletion and last-admin safeguards), registration approval/rejection with custom reasons, tuition payment verification, training schedule management, and categorized announcements.
- **Dynamic Academy CMS:** Full control over the "About Us" page from the admin panel—including academy mission/vision, features, facilities, coaches, age groups, achievements, statistics, and photo gallery—with secure file naming and automatic cleanup of deleted media.
- **Custom Error Pages:** Dedicated templates for HTTP `403` and `404` responses.
- **Database Migrations & Seeding:** Schema versioning via Alembic (`Flask-Migrate`) and initial data setup via `seed.py`.

---

## Application Flow

1. **Player / Parent Journey:** Create account → Log in → Complete 6-step registration & upload documents → Wait for admin review → Complete tuition payment → Wait for payment approval → Select a weekly training shift.
2. **Admin Journey:** Access admin dashboard → Review pending player registrations (approve/reject with reason) → Verify tuition payments → Manage training schedules, announcements, users, and academy CMS content.

---

## Tech Stack

- **Backend:** Python, Flask, Flask-Login, Flask-Limiter, Werkzeug
- **Database & ORM:** SQLAlchemy, Flask-SQLAlchemy, Alembic (Flask-Migrate), SQLite (development), PostgreSQL (production)
- **Forms & Validation:** Flask-WTF, WTForms
- **Frontend:** Jinja2 Templates, HTML5, CSS3 (RTL), Vanilla JavaScript, Font Awesome
- **Deployment:** Gunicorn

---

## Project Structure

```text
Mellipooshan-football-academy/
├── admin/                   # Admin blueprint, forms, and management routes
├── auth/                    # Authentication blueprint (signup, login, logout)
├── enrollment/              # Multi-step player registration and document uploads
├── panel/                   # Player/parent dashboard, profile, and training selection
├── migrations/              # Alembic database migration scripts
├── static/
│   ├── CSS/                 # Modular stylesheets (public, auth, panel, admin)
│   ├── JS/                  # Interactive scripts (base, profile, registration)
│   └── images/              # Static assets and academy logo
├── templates/
│   ├── admin/               # Admin dashboard and CMS templates
│   ├── auth/                # Login and signup templates
│   ├── enrollment/          # Multi-step course registration template
│   ├── error/               # Custom 403 and 404 error pages
│   └── panel/               # Player panel templates
├── app.py                   # Application entry point
├── config.py                # Development and production configurations
├── extensions.py            # Flask extensions initialization
├── models.py                # SQLAlchemy database models
├── security_utils.py        # Admin decorators, safe URL checks, and secure file handling
├── seed.py                  # Initial database seeding script
├── requirements.txt         # Python dependencies
└── .gitignore
```

---

## Getting Started

### Prerequisites

- Python 3.10+ (recommended)
- `pip` and `venv`

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/alireza-oman/Mellipooshan-football-academy.git
   cd Mellipooshan-football-academy
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # Linux / macOS
   python3 -m venv venv
   source venv/bin/activate

   # Windows (PowerShell)
   python -m venv venv
   venv\Scripts\Activate.ps1
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   Create a `.env` file in the project root:
   ```env
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=sqlite:///academy.db
   ```
   > **Security Note:** Never commit your `.env` file, real credentials, or production database URLs to Git. For production deployments, use PostgreSQL and serve the app with Gunicorn (`gunicorn app:app`).

5. **Initialize the database and seed initial data:**
   ```bash
   # Apply database migrations (if using Alembic)
   flask db upgrade

   # Seed initial data
   python seed.py
   ```

6. **Start the application:**
   ```bash
   python app.py
   ```
   The application will be available at `http://127.0.0.1:5000`.

---

## Database Models Overview

| Model | Description |
| :--- | :--- |
| `User` | Registered player/parent and administrator accounts |
| `ClubRegistration` | Player enrollment records, uploaded documents, approval status, and payment status |
| `Training` | Weekly training shifts, age groups, venues, and schedules |
| `Announcement` | Categorized academy notices with priority/importance flags |
| `AboutUsMain` | Core academy introduction, mission, vision, and CTA content |
| `AboutFeature` & `AboutFacility` | Academy highlights and training facilities |
| `Coach` | Coaching staff profiles, roles, bios, and photos |
| `AboutAgeGroup` | Supported academy age categories |
| `Achievement` & `AboutStat` | Club honors, trophies, and key numerical statistics |
| `GalleryItem` | Categorized media gallery images (trainings, matches, ceremonies) |

---

## License

All rights reserved unless otherwise specified. This project is developed as a portfolio and practical backend web application.

---

<div id="mellipooshan-football-academy-persian" dir="rtl">

# سامانه مدیریت و ثبت‌نام آکادمی فوتبال ملی‌پوشان

یک وب‌اپلیکیشن یکپارچه و ماژولار ساخته‌شده با **Python** و **Flask** برای مدیریت آکادمی فوتبال و ثبت‌نام آنلاین بازیکنان. این سامانه با رابط کاربری کاملاً راست‌چین (RTL) و واکنش‌گرا طراحی شده و شامل احراز هویت با شماره موبایل، ثبت‌نام چندمرحله‌ای همراه با آپلود مدارک، بررسی و تأیید شهریه، انتخاب شیفت تمرینی هفتگی، سیستم اطلاعیه‌رسانی و پنل مدیریت اختصاصی با قابلیت مدیریت محتوا (CMS) است.

---

## ویژگی‌ها

- **احراز هویت و امنیت:** ثبت‌نام و ورود مبتنی بر شماره موبایل با `Flask-Login`، رمزنگاری امن رمز عبور (Werkzeug)، قابلیت «مرا به خاطر بسپار»، اعتبارسنجی ریدایرکت‌های امن، محافظت CSRF با `Flask-WTF` و محدودسازی نرخ درخواست‌ها با `Flask-Limiter`.
- **ثبت‌نام آنلاین چندمرحله‌ای:** فرم هوشمند ۶ مرحله‌ای برای ثبت مشخصات بازیکن، اطلاعات ولی، سابقه ورزشی، آدرس و آپلود مدارک موردنیاز (عکس پرسنلی، شناسنامه، بیمه ورزشی و رضایت‌نامه).
- **پنل اولیا و بازیکنان:** داشبورد شخصی برای رهگیری وضعیت پرونده (همراه با مشاهده علت رد احتمالی)، پیگیری وضعیت پرداخت شهریه، انتخاب شیفت تمرینی هفتگی پس از تأیید شهریه، مشاهده اطلاعیه‌ها و مدیریت پروفایل، رمز عبور و آواتار.
- **پنل مدیریت ارشد:** داشبورد آماری با دسترسی محدود به ادمین، مدیریت کاربران همراه با صفحه‌بندی (با محافظت در برابر حذف خود و حذف آخرین ادمین)، بررسی و تأیید یا رد پرونده‌های ثبت‌نام با ذکر دلیل، تأیید یا رد پرداخت‌ها، برنامه‌ریزی شیفت‌های تمرینی و انتشار اطلاعیه‌های دسته‌بندی‌شده.
- **سیستم مدیریت محتوای پویا (CMS):** مدیریت کامل بخش‌های صفحه «درباره ما» از جمله معرفی، مأموریت و چشم‌انداز، ویژگی‌ها، امکانات، مربیان، رده‌های سنی، افتخارات، آمارها و گالری تصاویر همراه با ذخیره‌سازی امن فایل‌ها و پاکسازی خودکار رسانه‌های حذف‌شده.
- **صفحات خطای اختصاصی:** قالب‌های طراحی‌شده برای خطاهای `403` و `404`.
- **مدیریت دیتابیس و داده‌های اولیه:** مدیریت تغییرات ساختار دیتابیس با `Alembic` (`Flask-Migrate`) و مقداردهی اولیه با اسکریپت `seed.py`.

---

## جریان کار سیستم

1. **مسیر بازیکن / ولی:** ایجاد حساب کاربری ← ورود به سیستم ← تکمیل فرم ۶ مرحله‌ای و آپلود مدارک ← بررسی پرونده توسط مدیریت ← پرداخت شهریه ← تأیید پرداخت ← انتخاب شیفت تمرینی هفتگی.
2. **مسیر ادمین:** ورود به داشبورد مدیریت ← بررسی پرونده‌های در انتظار تأیید (تأیید یا رد با ثبت علت) ← بررسی و تأیید شهریه‌ها ← مدیریت شیفت‌های تمرینی، اطلاعیه‌ها، کاربران و محتوای صفحه درباره ما.

---

## تکنولوژی‌های استفاده‌شده

- **بک‌اند:** Python, Flask, Flask-Login, Flask-Limiter, Werkzeug
- **دیتابیس و ORM:** SQLAlchemy, Flask-SQLAlchemy, Alembic (Flask-Migrate)، SQLite (توسعه)، PostgreSQL (محیط واقعی)
- **فرم‌ها و اعتبارسنجی:** Flask-WTF, WTForms
- **فرانت‌اند:** Jinja2 Templates, HTML5, CSS3 (RTL), Vanilla JavaScript, Font Awesome
- **استقرار (Deployment):** Gunicorn

---

## راهنمای نصب و اجرا

### پیش‌نیازها

- پایتون نسخه `3.10` یا بالاتر
- `pip` و `venv`

### مراحل راه‌اندازی

1. **کلون کردن پروژه:**

<div dir="ltr">

```bash
git clone https://github.com/alireza-oman/Mellipooshan-football-academy.git
cd Mellipooshan-football-academy
```

</div>

2. **ساخت و فعال‌سازی محیط مجازی:**

<div dir="ltr">

```bash
# Linux / macOS
python3 -m venv venv
source venv/bin/activate

# Windows (PowerShell)
python -m venv venv
venv\Scripts\Activate.ps1
```

</div>

3. **نصب وابستگی‌ها:**

<div dir="ltr">

```bash
pip install -r requirements.txt
```

</div>

4. **تنظیم متغیرهای محیطی:**
   یک فایل با نام `.env` در ریشه پروژه بسازید و مقادیر زیر را در آن قرار دهید:

<div dir="ltr">

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///academy.db
```

</div>

   > **نکته امنیتی:** هرگز فایل `.env`، رمزهای عبور یا اطلاعات دیتابیس واقعی را روی گیت کامیت نکنید. برای استقرار در محیط واقعی از PostgreSQL و `gunicorn app:app` استفاده کنید.

5. **آماده‌سازی دیتابیس و داده‌های اولیه:**

<div dir="ltr">

```bash
# اجرای مایگریشن‌های دیتابیس
flask db upgrade

# ایجاد داده‌های اولیه
python seed.py
```

</div>

6. **اجرای برنامه:**

<div dir="ltr">

```bash
python app.py
```

</div>

   برنامه روی آدرس `http://127.0.0.1:5000` در دسترس خواهد بود.

---

## لایسنس

تمامی حقوق این پروژه محفوظ است (All Rights Reserved)، مگر اینکه خلاف آن ذکر شده باشد. این پروژه به‌عنوان یک نمونه کار عملی در حوزه توسعه بک‌اند طراحی و پیاده‌سازی شده است.

</div>
