[English](#mellipooshan-football-academy) | [فارسی](#mellipooshan-football-academy-persian)

# Mellipooshan Football Academy

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-000000?logo=flask&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Production%20DB-336791?logo=postgresql&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Local%20DB-003B57?logo=sqlite&logoColor=white)

A full-stack football academy management and online player registration platform built with **Python** and **Flask**. It supports user authentication, multi-step online player registration with document uploads, payment status tracking, training session selection, announcements, and a dedicated administration panel.

---

## Features

- **User Authentication:** Registration, login, remember-me authentication, profile management, avatar upload, password change, and account activation/deactivation powered by `Flask-Login` and `Flask-WTF`.
- **Multi-Step Player Registration:** Guided onboarding capturing player personal details, parent/guardian info, football background/playing position, contact details, and required document uploads.
- **Player Panel:** Personal dashboard displaying registration status, payment verification status, training session selection, and academy announcements.
- **Administration Panel:** Custom dashboard with system statistics, user management, registration approval/rejection, payment status updates, training session management, and announcements.
- **Dynamic Academy CMS:** Full management of academy info, coaches, age groups, facilities, achievements, statistics, and gallery items.
- **Security Hardening:** Password hashing via `Werkzeug`, CSRF protection via `Flask-WTF`, role-based access control (RBAC), secure filename sanitization, ownership checks, POST-only sensitive actions, and safe redirect URL validation.
- **Responsive RTL Frontend:** Dark football-themed interface tailored for Persian users with right-to-left layout, Vazirmatn & Teko typography, mobile navigation, and toast notifications.
- **Database Migrations:** Version-controlled schema management via `Alembic` (`Flask-Migrate`).

---

## Application Flow

1. **Player Journey:** Create account → Login → Complete multi-step registration → Upload documents → Submit registration → Wait for admin approval → Complete payment → Payment approved → Select training session.
2. **Admin Journey:** Access admin panel → Review dashboard metrics & incoming registrations → Approve/reject players & verify payments → Manage training sessions, announcements & academy CMS content.

---

## Tech Stack

- **Backend:** Python, Flask, Flask-Login, Flask-WTF, WTForms, Werkzeug
- **Database & ORM:** SQLAlchemy, Alembic (Flask-Migrate), SQLite (Local), PostgreSQL (Production)
- **Frontend:** Jinja2 Templates, HTML5, CSS3, Vanilla JavaScript, Font Awesome
- **Deployment:** Gunicorn, Render, PostgreSQL

---

## Project Structure

```text
Mellipooshan-football-academy/
├── admin/                  # Admin blueprint (dashboard, approvals, CMS management)
│   ├── __init__.py
│   ├── forms.py
│   └── routes.py
├── auth/                   # Authentication blueprint (login, register, logout)
│   ├── __init__.py
│   ├── forms.py
│   └── routes.py
├── enrollment/             # Player registration, file uploads & payment workflow
│   ├── __init__.py
│   ├── forms.py
│   └── routes.py
├── panel/                  # Player dashboard, profile & training selection
│   ├── __init__.py
│   ├── forms.py
│   └── routes.py
├── migrations/             # Alembic database migration scripts
├── static/                 # Static assets (CSS, JS, images)
├── templates/              # Jinja2 HTML templates organized by blueprint
├── app.py                  # Application factory & entry point
├── config.py               # Environment-based configuration
├── extensions.py           # Flask extensions initialization
├── models.py               # SQLAlchemy ORM models
├── security_utils.py       # Custom security helpers & validators
├── seed.py                 # Database seeding script
├── requirements.txt        # Python dependencies
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
   git clone [https://github.com/alireza-oman/Mellipooshan-football-academy.git](https://github.com/alireza-oman/Mellipooshan-football-academy.git)
   cd Mellipooshan-football-academy
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # Linux / macOS
   python3 -m venv .venv
   source .venv/bin/activate

   # Windows (Command Prompt)
   python -m venv .venv
   .venv\Scripts\activate

   # Windows (PowerShell)
   python -m venv .venv
   .venv\Scripts\Activate.ps1
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
   > **Security Note:** Never commit your `.env` file or real credentials to Git.

5. **Run database migrations:**
   ```bash
   flask db upgrade
   ```

6. **Start the application:**
   ```bash
   flask run
   ```
   The application will be available at `http://127.0.0.1:5000`.

### Production Deployment

For production environments (such as Render), configure `SECRET_KEY` and a `PostgreSQL` `DATABASE_URL`, then serve with Gunicorn:
```bash
gunicorn app:app
```

---

## Database Models Overview

| Model | Description |
| :--- | :--- |
| `User` | Registered player and administrator accounts |
| `ClubRegistration` | Multi-step player enrollment records, documents, and approval/payment statuses |
| `Training` | Available academy training schedules and sessions |
| `Announcement` | Official academy news and announcements |
| `AboutUsMain` / `AboutFeature` / `AboutFacility` | Academy overview, core features, and facility details |
| `Coach` / `AboutAgeGroup` | Coaching staff profiles and age-group categories |
| `Achievement` / `AboutStat` / `GalleryItem` | Academy honors, key statistics, and media gallery |

---

## Roadmap / Future Improvements

- [ ] Add automated unit and integration tests (`pytest`)
- [ ] Add `.env.example` for easier onboarding
- [ ] Implement online payment gateway integration alongside manual verification
- [ ] Optimize static image assets (e.g., WebP compression)

---

## License

Copyright © 2026 Alireza. All rights reserved.
This software is proprietary and developed exclusively for Mellipooshan Football Academy. It is published here solely for portfolio showcase purposes; unauthorized copying, distribution, or modification is strictly prohibited.

---

<div id="mellipooshan-football-academy-persian" dir="rtl">

# آکادمی فوتبال ملی‌پوشان (Mellipooshan Football Academy)

یک وب‌اپلیکیشن فول‌استک ساخته‌شده با **Python** و **Flask** برای مدیریت آکادمی فوتبال و ثبت‌نام آنلاین بازیکنان. این سامانه شامل احراز هویت کاربران، فرم ثبت‌نام چندمرحله‌ای همراه با بارگذاری مدارک، پیگیری وضعیت تایید و پرداخت، انتخاب سانس تمرینی و پنل مدیریت اختصاصی است.

---

## ویژگی‌ها

- **احراز هویت کاربران:** ثبت‌نام، ورود، قابلیت «مرا به خاطر بسپار»، مدیریت پروفایل، آپلود آواتار، تغییر رمز عبور و فعال/غیرفعال‌سازی حساب‌ها با `Flask-Login` و `Flask-WTF`.
- **ثبت‌نام آنلاین چندمرحله‌ای:** دریافت گام‌به‌گام اطلاعات فردی بازیکن، مشخصات والدین، سوابق فوتبالی و پست بازی، اطلاعات تماس و بارگذاری مدارک.
- **پنل اختصاصی بازیکن:** داشبورد کاربری برای مشاهده وضعیت ثبت‌نام، وضعیت تایید پرداخت، انتخاب سانس تمرینی و مشاهده اطلاعیه‌ها.
- **پنل مدیریت اختصاصی:** داشبورد آماری سیستم، مدیریت کاربران، تایید یا رد ثبت‌نام‌ها، مدیریت وضعیت پرداخت‌ها، تعریف سانس‌های تمرینی و انتشار اطلاعیه‌ها.
- **مدیریت محتوای آکادمی (CMS):** مدیریت پویا برای معرفی آکادمی، مربیان، رده‌های سنی، امکانات، افتخارات، آمارها و گالری تصاویر.
- **امنیت و حفاظت داده‌ها:** هش کردن رمزها با `Werkzeug`، محافظت CSRF با `Flask-WTF`، کنترل دسترسی مبتنی بر نقش، ایمن‌سازی نام فایل‌های آپلودی، بررسی مالکیت رکوردها و اعتبارسنجی آدرس‌های بازگشتی.
- **رابط کاربری راست‌به‌چپ (RTL):** طراحی تیره و واکنش‌گرا با فونت‌های وزیرمتن و Teko، منوی موبایل و اعلان‌های Toast.
- **مدیریت تغییرات دیتابیس:** مایگریشن‌های نسخه‌بندی‌شده با `Alembic` (`Flask-Migrate`).

---

## جریان کار سیستم

1. **مسیر بازیکن:** ایجاد حساب کاربری ← ورود ← تکمیل فرم چندمرحله‌ای ← بارگذاری مدارک ← ارسال درخواست ← تایید ثبت‌نام توسط ادمین ← پرداخت شهریه ← تایید پرداخت ← انتخاب سانس تمرینی.
2. **مسیر ادمین:** ورود به پنل مدیریت ← بررسی آمار داشبورد و ثبت‌نام‌های جدید ← تایید یا رد بازیکنان و بررسی پرداخت‌ها ← مدیریت سانس‌ها، اطلاعیه‌ها و محتوای سایت.

---

## تکنولوژی‌های استفاده‌شده

- **بک‌اند:** Python, Flask, Flask-Login, Flask-WTF, WTForms, Werkzeug
- **دیتابیس و ORM:** SQLAlchemy, Alembic (Flask-Migrate), SQLite (محیط توسعه), PostgreSQL (محیط عملیاتی)
- **فرانت‌اند:** Jinja2 Templates, HTML5, CSS3, Vanilla JavaScript, Font Awesome
- **استقرار (Deployment):** Gunicorn, Render, PostgreSQL

---

## راهنمای نصب و اجرا

### پیش‌نیازها

- پایتون نسخه `3.10` یا بالاتر
- `pip` و `venv`

### مراحل راه‌اندازی

1. **کلون کردن پروژه:**

<div dir="ltr">

```bash
git clone [https://github.com/alireza-oman/Mellipooshan-football-academy.git](https://github.com/alireza-oman/Mellipooshan-football-academy.git)
cd Mellipooshan-football-academy
```

</div>

2. **ساخت و فعال‌سازی محیط مجازی:**

<div dir="ltr">

```bash
# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate

# Windows (Command Prompt)
python -m venv .venv
.venv\Scripts\activate

# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1
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

   > **نکته امنیتی:** هرگز فایل `.env` یا کلیدهای واقعی خود را روی گیت کامیت نکنید.

5. **اجرای مایگریشن‌های دیتابیس:**

<div dir="ltr">

```bash
flask db upgrade
```

</div>

6. **اجرای برنامه:**

<div dir="ltr">

```bash
flask run
```

</div>

   برنامه روی آدرس `http://127.0.0.1:5000` در دسترس خواهد بود.

---

## نقشه راه و بهبودهای آینده

- [ ] افزودن تست‌های خودکار با `pytest`
- [ ] افزودن فایل `.env.example` برای راه‌اندازی سریع‌تر
- [ ] اتصال به درگاه پرداخت آنلاین در کنار بررسی دستی
- [ ] بهینه‌سازی حجم تصاویر استاتیک (تبدیل به WebP)

---
## لایسنس

تمامی حقوق این نرم‌افزار متعلق به توسعه‌دهنده و آکادمی فوتبال ملی‌پوشان است. این مخزن صرفاً جهت نمایش در نمونه‌کار (پورتفولیو) منتشر شده و هرگونه کپی‌برداری، انتشار یا استفاده غیرمجاز بدون اجازه کتبی ممنوع می‌باشد..

</div>
