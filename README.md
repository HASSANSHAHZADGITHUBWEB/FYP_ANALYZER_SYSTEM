# 🎓 FYP Analyzer System – QAU (IIT Deployment)

This is a lightweight Final Year Project (FYP) Analyzer system developed using **Python (Django Framework)** along with **static frontend technologies (HTML/CSS)**. It is designed specifically for **university faculty and coordinators**, making the FYP evaluation and tracking process smoother, more organized, and efficient.

---

## 📚 Features

✅ **Admin Access**  
- Add Groups  
- Add Users  
- Add Designations (e.g., Coordinator, Faculty)  
- View All Group Responses  

✅ **Faculty Access**  
- Add Marks (Poster, Project, etc.)  
- View Average Marks of Groups  

---

## 🔒 Middleware Role Management

| Role       | Features Allowed |
|------------|------------------|
| **Admin**  | Add Groups, Add User, Add Designation, View All Responses |
| **Faculty**| Add Marks, View Average Marks Only |

---

## 🎯 Use Case
This system is specially designed for **QAU IIT department coordinators** to streamline the management of group evaluations, marking, and reporting. It ensures clear role separation and efficient recordkeeping.

---

## 🛠️ Installation & Setup Instructions

### 📦 1. Clone the Repository
```bash
git clone https://github.com/your-username/fyp-analyzer.git
cd fyp-analyzer
⚙️ 3. Configure Database in settings.py
Set up MySQL, PostgreSQL, or SQLite (default)

Update DATABASES section in settings.py accordingly
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
