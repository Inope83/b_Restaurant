@echo off
echo ========================================
echo Hotel Management System - Quick Start
echo ========================================

echo.
echo Step 1: Creating migrations...
python manage.py makemigrations accounts
python manage.py makemigrations rooms
python manage.py makemigrations dashboard

echo.
echo Step 2: Applying migrations...
python manage.py migrate

echo.
echo Step 3: Creating sample data...
python init_db.py

echo.
echo Step 4: Starting server...
echo.
echo ========================================
echo SUCCESS! Server starting...
echo Visit: http://127.0.0.1:8000
echo Admin: http://127.0.0.1:8000/admin
echo Login: admin / admin123
echo ========================================
echo.
python manage.py runserver

pause