@echo off
echo Starting Face Recognition Service with FaceNet PyTorch...

REM Check if virtual environment exists
if not exist venv_py312 (
    echo Virtual environment not found. Please run setup_pytorch.bat first.
    pause
    exit /b 1
)

REM Activate virtual environment and run the service
call venv_py312\Scripts\activate.bat
echo Starting FastAPI service on port 8003...
python -m uvicorn facenet_pytorch_service:app --reload --host 127.0.0.1 --port 8003

pause 