# Django Teacher Web app

This project is a **secure, logic-driven teacher Web app** built using Django that allows authenticated teachers to manage a list of students along with their subjects and marks.

---

## 🚀 Features

### 🔐 Custom Authentication System *(No Django auth used)*
- Passwords are **hashed and salted manually**
- Sessions are **handled without Django’s auth middleware**

### 🧑‍🏫 Teacher Dashboard
- Displays a list of students
- Inline edit & delete for student marks
- Logs all edits with user info and timestamp

### ➕ Add Student
- Dynamic modal popup to add students
- If student exists (same name & subject), merges marks using logic
- Rejects marks **> 100**

### 🔐 Security Features
- Manual **CSRF protection**
- **Parameterized DB queries** to avoid SQL Injection
- **XSS-safe input handling**
- Strict validation on **client & server**

---

## 🛠 Tech Stack

- **Backend:** Python, Django
- **Frontend:** HTML, CSS, Bootstrap 5, JavaScript
- **Database:** SQLite (default, but easily switchable)

---

## ⚙️ Setup Instructions

1. **Clone the repository**
    ```bash
    git clone https://github.com/Shreeharshahs/assessment.git
    cd cms
    ```

2. **Create virtual environment and install dependencies**
    ```bash
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    ```

3. **Apply migrations**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

4. **Run the server**
    ```bash
    python manage.py runserver
    ```

    Then open your browser and go to:  
    👉 [http://127.0.0.1:8000/register/]
        Once register login using the same.
        (http://127.0.0.1:8000/)

---

## 🔐 Custom Login Credentials

Register a new teacher using the `/register` route or manually via the Django admin or database.

---

## 🔒 Security Considerations

- Passwords are stored using **manual hashing** (`hashlib` + salt)
- Sessions are managed through **signed cookies**
- All inputs are **server-side validated**
- SQL operations use **Django ORM** (inherently safe)
- **XSS prevention** via escaping & safe rendering
- Custom **CSRF tokens** generated for each POST request

---

## 📝 Audit Logs

All mark updates are recorded in an `AuditLog` table with:
- Timestamp
- Teacher info
- Student name & subject
- Remarks

---

## 🧩 Challenges Faced

- Implementing **secure session handling manually**
- Creating a **modal** that handles both new and duplicate student logic cleanly
- Ensuring **validations** are enforced on both client and server

---

## ⏱ Time Taken

> Approximate time to complete: **14 hours**

---


