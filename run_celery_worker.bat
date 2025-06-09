@echo off
cd /d "D:\project\Missing-persons-project"
echo Activating virtual environment...
call new_venv\Scripts\activate.bat

echo Checking and installing required packages...
pip install celery==4.4.7 redis==3.5.3

echo.
echo Starting Celery worker...
echo.
echo If the worker starts successfully, you will see a list of tasks and a message saying "[...]: Ready".
echo The worker will continue running in this window. Do not close it.
echo.
celery -A config worker -l info
pause 