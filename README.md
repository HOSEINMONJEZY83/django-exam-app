# 🧪 Django Exam App

A web-based exam management system built with Django, featuring timed exams, teacher-student assignment, Excel report export with date range, and secure access control.

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

- User registration with role selection (Student or Teacher)

- Multi-teacher selection during student registration (with Ctrl/Cmd for multiple selection)

- Teacher dashboard to create, manage, and monitor exams

- Timed exams with start and end date/time restrictions

- Prevention of unauthorized access to exams via URL manipulation

- One-time attempt per student for each exam

- Automatic scoring and result calculation

- Validation to prevent empty messages (text or file required)

- Detailed result page showing correct/incorrect answers

- Responsive UI for both students and teachers

- Excel report export for exam results by teacher with custom date range selection

## ❓ FAQ

#### 📌 What features does your project have?

The project allows users to register as a student or teacher, create and manage timed exams, and participate in exams within their allowed time frame. Students can only access exams created by their assigned teachers, and results are calculated automatically.
#### 📌 Can teachers participate in their own exams?

No, teachers cannot take their own exams
#### 📌 How are exam times managed?

Exams have start and end times. Students can only access them within this time range.
#### 📌 Can students take an exam multiple times?

No, each student can attempt an exam only once.

#### 📌 How is exam access controlled?

Students can only access exams from their own teachers, and direct URL manipulation to access other exams is blocked

## Feedback

I am happy to send your comments to my email. HOSEINMONJEZY1383@gmail.com
