@echo off
cd /d "D:\project\Missing-persons-project"
echo Activating virtual environment...
call new_venv\Scripts\activate.bat

echo Creating temporary __init__.py without Celery import...
echo # Temporarily removed Celery import > config\__init__.py.bak
copy config\__init__.py config\__init__.py.original
echo # Celery import temporarily disabled > config\__init__.py

echo Starting Django server...
python manage.py runserver
echo.
echo If the server exited unexpectedly, check for errors above.

echo Restoring original __init__.py...
copy config\__init__.py.original config\__init__.py
del config\__init__.py.original
del config\__init__.py.bak

pause 