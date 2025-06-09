@echo off
cd /d "D:\project\Missing-persons-project"
echo Activating virtual environment...
call new_venv\Scripts\activate.bat

echo Checking for required packages...
python -c "import importlib.util; celery_spec = importlib.util.find_spec('celery'); print('Celery is ' + ('installed' if celery_spec else 'NOT INSTALLED'))"

REM Check if Celery is missing and offer to run without it
IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo Celery package not found. Would you like to:
    echo 1. Install Celery and continue
    echo 2. Run Django without Celery
    echo.
    choice /C 12 /N /M "Enter your choice (1 or 2): "
    
    IF ERRORLEVEL 2 (
        echo.
        echo Running Django without Celery integration...
        echo # Celery import temporarily disabled > config\__init__.py.bak
        copy config\__init__.py config\__init__.py.original
        echo # Celery import temporarily disabled > config\__init__.py
        echo.
    ) ELSE (
        echo.
        echo Installing Celery...
        pip install celery==4.4.7 redis==3.5.3
        echo.
    )
)

echo Starting Django server...
python manage.py runserver
echo.
echo Server has stopped.

REM Restore original config file if we modified it
IF EXIST config\__init__.py.original (
    echo Restoring original config file...
    copy config\__init__.py.original config\__init__.py
    del config\__init__.py.original
    del config\__init__.py.bak
)

echo.
echo If the server exited unexpectedly, check for errors above.
pause 