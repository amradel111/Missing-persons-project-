@echo off
echo Starting Face Recognition Service with PyTorch Implementation...
echo This service will run on port 8003

cd /d "%~dp0"
cd face_recognition_service
call venv_py312\Scripts\activate.bat
python -m uvicorn facenet_pytorch_service:app --host 127.0.0.1 --port 8003

pause 