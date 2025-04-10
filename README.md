# 🧠 Django Quiz App

A web-based quiz platform built with **Django** and styled using **Tailwind CSS**.  
Users can create quizzes with questions and answers, assign categories and difficulty levels, and search through quizzes.

---

## 🚀 Features

- User login and quiz creation
- Assign **categories** and **difficulty levels**
- Edit questions and answers
- Search and filter quizzes
- Responsive UI with Tailwind CSS
- Admin panel
- Contact form and notifications
- Database seeding with test data

---

## 📦 Tech Stack

- Python 3.10+
- Django 4.x
- Tailwind CSS (via `django-tailwind`)
- SQLite (default DB)

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/quiz-app.git
cd quiz-app
```

### 2. Create and activate virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

---

## 🎨 Tailwind CSS Setup

### 4. Initialize Tailwind (first-time only)

```bash
python manage.py tailwind init theme
```

In `settings.py`, set:

```python
TAILWIND_APP_NAME = 'theme'
INTERNAL_IPS = ['127.0.0.1']
```

Then run inside `theme/` directory:

```bash
npm install
```

### 5. Start Tailwind watcher (in a separate terminal tab)

```bash
python manage.py tailwind start
```

> This watches your Tailwind CSS and auto-compiles it.

---

## 🛠️ Database Setup

### 6. Apply migrations

```bash
python manage.py migrate
```

### 7. (Optional) Seed sample data

```bash
python manage.py seed_data
```

Creates:
- Sample categories
- 3 quizzes (each with questions/answers)
- A test user `testuser` with password `testpass123`

---

### 8. Create superuser (optional)

```bash
python manage.py createsuperuser
```

---

## ▶️ Running the Project

To run the development server:

```bash
python manage.py runserver
```

Then visit:  
http://127.0.0.1:8000/

---

## 🧪 Test Login

| Username  | Password     |
|-----------|--------------|
| testuser  | testpass123  |

---

## 🧼 Wipe the database

```bash
python manage.py flush
```

> Or delete `db.sqlite3` and re-run `migrate`

