# Mellipooshan Football Academy

A full-stack football academy management and online registration platform built with **Python and Flask**.

The platform provides an online registration system for players, user accounts, player management, training session selection, payment status management, announcements, and a dedicated administration panel.

## Features

### User Authentication

* User registration and login
* Secure password hashing
* Remember-me authentication
* Account activation/deactivation
* Profile management
* Password change
* Profile avatar upload
* Role-based access for administrators

### Online Player Registration

* Multi-step registration form
* Player personal information
* Parent/guardian information
* Football background and playing position
* Address and contact information
* Document and image uploads
* Registration status tracking
* Form validation
* CSRF protection

### Player Panel

* Personal dashboard
* Registration status
* Payment status
* Training session selection
* Announcements
* Profile management
* Avatar management
* Password management

### Administration Panel

* Dashboard with system statistics
* User management
* Player registration management
* Registration approval/rejection
* Payment status management
* Training session management
* Announcement management
* Academy information management
* Coaches management
* Age-group management
* Achievements management
* Statistics management
* Gallery management

### Frontend

* Responsive design
* RTL layout for Persian users
* Multi-step registration interface
* Mobile navigation
* Toast notifications
* Scroll animations
* Responsive admin and user panels
* Modern football-themed UI
* Vazirmatn and Teko typography
* Font Awesome icons

## Technology Stack

### Backend

* Python
* Flask
* Flask-SQLAlchemy
* Flask-Login
* Flask-WTF
* Flask-Migrate
* WTForms
* SQLAlchemy
* Werkzeug

### Database

* SQLite for local development
* PostgreSQL for production

### Frontend

* HTML5
* CSS3
* JavaScript
* Jinja2
* Font Awesome

### Deployment

* Gunicorn
* Render
* PostgreSQL

## Project Structure

```text
Mellipooshan-football-academy/
│
├── admin/
│   ├── __init__.py
│   ├── forms.py
│   └── routes.py
│
├── auth/
│   ├── __init__.py
│   ├── forms.py
│   └── routes.py
│
├── enrollment/
│   ├── __init__.py
│   ├── forms.py
│   └── routes.py
│
├── panel/
│   ├── __init__.py
│   ├── forms.py
│   └── routes.py
│
├── migrations/
│
├── static/
│   ├── CSS/
│   ├── JS/
│   └── images/
│
├── templates/
│   ├── admin/
│   ├── auth/
│   ├── enrollment/
│   ├── panel/
│   └── ...
│
├── app.py
├── config.py
├── extensions.py
├── models.py
├── security_utils.py
├── seed.py
├── requirements.txt
└── README.md
```

## Application Architecture

The application uses Flask Blueprints to separate the major parts of the system:

```text
Application
│
├── Authentication
│   ├── Login
│   ├── Registration
│   └── Logout
│
├── Player Panel
│   ├── Dashboard
│   ├── Profile
│   ├── Registrations
│   └── Training Selection
│
├── Enrollment
│   ├── Player Registration
│   ├── File Uploads
│   └── Payment Workflow
│
└── Administration
    ├── Users
    ├── Registrations
    ├── Payments
    ├── Trainings
    ├── Announcements
    └── Academy Content
```

## Security

The project includes several security mechanisms:

* Password hashing using Werkzeug
* CSRF protection with Flask-WTF
* Authentication with Flask-Login
* Role-based authorization for administrators
* Secure file naming for uploaded files
* Protected administrative routes
* Ownership checks for player registrations
* POST requests for sensitive actions
* Safe redirect URL validation
* Secure session cookie configuration

## Database Models

The application uses SQLAlchemy ORM for database management.

Major entities include:

* `User`
* `ClubRegistration`
* `Training`
* `Announcement`
* `AboutUsMain`
* `AboutFeature`
* `AboutFacility`
* `Coach`
* `AboutAgeGroup`
* `Achievement`
* `AboutStat`
* `GalleryItem`

Relationships between users, player registrations, and training sessions are handled through SQLAlchemy.

## Local Development

### 1. Clone the repository

```bash
git clone https://github.com/alireza-oman/Mellipooshan-football-academy.git
cd Mellipooshan-football-academy
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file and configure the required application settings.

Example:

```env
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///academy.db
```

For production, use a PostgreSQL connection string instead of SQLite.

### 5. Run the application

```bash
flask run
```

The application will be available at:

```text
http://127.0.0.1:5000
```

## Production Deployment

The application can be deployed using **Gunicorn** with PostgreSQL.

Example:

```bash
gunicorn app:app
```

For production environments, configure:

* `SECRET_KEY`
* `DATABASE_URL`
* PostgreSQL database
* Secure HTTPS configuration

## User Workflow

A typical player registration workflow looks like this:

```text
Create Account
      ↓
Login
      ↓
Complete Player Registration
      ↓
Upload Required Documents
      ↓
Submit Registration
      ↓
Admin Review
      ↓
Registration Approved
      ↓
Payment
      ↓
Payment Approved
      ↓
Select Training Session
```

## Admin Workflow

Administrators can manage the main operational parts of the academy:

```text
Dashboard
   │
   ├── Users
   ├── Player Registrations
   ├── Payments
   ├── Training Sessions
   ├── Announcements
   └── Academy Content
          ├── Coaches
          ├── Age Groups
          ├── Facilities
          ├── Achievements
          ├── Statistics
          └── Gallery
```

## UI and Design

The interface is designed for a Persian-speaking football academy and uses an RTL layout.

The design focuses on:

* Dark football-inspired visual styling
* Responsive layouts
* Mobile-friendly navigation
* Clear registration steps
* Separate user and administration interfaces
* Persian typography
* Interactive UI elements

## Project Status

This project is an ongoing Flask-based football academy management system developed as a practical backend project.

It demonstrates experience with:

* Flask application architecture
* SQLAlchemy and relational databases
* Authentication and authorization
* Form validation
* File uploads
* Administrative systems
* Responsive frontend integration
* Production deployment

## License

This project is currently intended as a personal portfolio and learning project.

All rights reserved unless otherwise specified.
