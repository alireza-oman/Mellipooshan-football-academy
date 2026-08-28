# ⚽ Mellipooshan Football Academy — Management & Registration System

A modern and integrated web application for youth football academies and schools, built with **Flask (Python)**, **SQLAlchemy**, and a fully responsive **RTL** interface.

## 🌟 Key Features

### 👨‍👩‍👦 Parents & Players Panel

* **Multi-Step Registration:** A smart 6-step registration form with a dedicated dropzone for document uploads:

  * Profile photo
  * Birth certificate
  * Sports insurance
  * Consent form
* **Application Tracking:** View application status and rejection reasons provided by administrators.
* **Tuition Payment & Training Schedule:** Select a fixed weekly training schedule after tuition approval.
* **User Profile:** Manage personal information, change passwords, and upload avatars with live preview.

### 👑 Admin Dashboard

* **Registration Management:** Review complete registration details, preview documents, and approve or reject applications with a reason.
* **Payment Management:** Review, approve, or cancel tuition payment requests.
* **Training Schedule Management:** Create, edit, and delete training sessions for different age groups.
* **Notification System:** Publish announcements with categories and priority levels.
* **Dynamic Content Management (CMS):** Manage About Us sections, coaches, achievements, statistics, and gallery content.
* **User Management:** View, update access levels, and delete users with pagination support.

## 🛠️ Technologies Used

### Backend

* Python 3
* Flask
* Flask-SQLAlchemy
* Flask-Login
* Flask-WTF
* Flask-Migrate

### Database

* SQLite
* Compatible with PostgreSQL and MySQL

### Frontend

* HTML5
* CSS3
* Vanilla JavaScript
* Jinja2
* FontAwesome 6

### Fonts

* Vazirmatn
* Teko

## 🚀 Local Setup

### 1. Clone the Repository

```bash
git clone https://github.com/alireza-oman/Mellipooshan-football-academy.git
cd Mellipooshan-football-academy
```

### 2. Create and Activate a Virtual Environment

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

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Initialize the Database and Seed Initial Data

```bash
python seed.py
```

### 5. Run the Application

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

## 👤 Default Admin Account

After running the project, a default admin user is created with administrative access.

* **Mobile Number:** `---`

> For production use, make sure to change the default login credentials.

## 📂 Project Structure

```text
football-academy/
│
├── admin/                    # Admin blueprint and management logic
├── auth/                     # Authentication blueprint
├── enrollment/               # Registration and document uploads
├── panel/                    # Player/user panel
│
├── static/
│   ├── css/                  # Global and panel styles
│   ├── js/                   # Interactive scripts
│   └── uploads/              # Uploaded images and documents
│
├── templates/                # Jinja2 templates
│
├── app.py                    # Main application entry point
├── config.py                 # Development and production configuration
├── extensions.py             # Flask extension instances
├── models.py                 # Database models
├── seed.py                   # Initial data creation
├── requirements.txt          # Python dependencies
├── .gitignore                # Ignored Git files
└── README.md                 # Project documentation
```

## 📌 GitHub Setup

If the project has not been connected to Git yet:

```bash
git init
git add .
git commit -m "Initial commit: Football Academy Management System"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
git push -u origin main
```

For future changes:

```bash
git add .
git commit -m "Update project"
git push
```

## 🔐 Security

Never store sensitive information directly in the source code.

Sensitive data such as:

* `SECRET_KEY`
* Admin passwords
* Database connection credentials
* API keys
* Payment gateway credentials

should be stored in environment variables or local configuration files and excluded using `.gitignore`.

