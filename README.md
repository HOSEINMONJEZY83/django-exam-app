# 🧪 Online Exam System (Django-based)

A simple online exam system built with Django. This project includes features like user registration with role selection (teacher/student), exam creation by teachers, exam participation by students, automatic grading, and exporting exam responses.

## Authors

- [HOSEINMONJEZY83](https://www.github.com/HOSEINMONJEZY83)

## 🚀 Quick Start

1. Clone the repository

```bash
git clone https://github.com/HOSEINMONJEZY83/django-exam-app.git
cd django-exam-app
```
2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```
3. Install dependencies

```bash
pip install -r requirements.txt
```
4. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```
5. Run the development server

```bash
python manage.py runserver
```

## ✨ Features

- User registration with role selection (teacher or student)

- Students can select multiple teachers during registration

- Students only see and can participate in exams created by their selected teachers

- Teachers are prevented from participating in any exams

- Exams can be scheduled with specific start and end times

- Students can participate in each exam only once

- Automatic grading and display of correct answers after the exam

- Protection against unauthorized access to exams via URL manipulation

- Teacher dashboard to create exams, add questions, and export student answers to Excel

- Simple and user-friendly interface built with Bootstrap

## 📦 Excel Export by Teachers

- Teachers can download an Excel file of student answers for their exams directly from their dashboard.

## ❓ FAQ

#### 📌 Can teachers participate in exams?

No, teachers are not allowed to take any exams.
##### 📌 Can a student see exams from all teachers?

No, students only see exams created by the teachers they selected during registration.
#### 📌 What if a student tries to access an exam URL directly?

The system verifies whether the exam belongs to the student's selected teachers; if not, access is denied.
#### 📌 How many times can a student take each exam?

Only once. After submitting answers, the student cannot retake the exam.

## Feedback

I am happy to send your comments to my email. HOSEINMONJEZY1383@gmail.com
