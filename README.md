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
git clone https://github.com/pawelwuuu/quizz-app.git
cd quiz-app
```

### 2. Install Python dependencies

```bash
django
django-tailwind
django-browser-reload
```
### 3. Run app
```bash
python manage.py runserver
```
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

