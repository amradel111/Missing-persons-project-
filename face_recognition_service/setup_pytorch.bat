@echo off
echo Setting up environment for FaceNet PyTorch...

REM Create a virtual environment with Python 3.12
if not exist venv_py312 (
    echo Creating Python 3.12 virtual environment...
    py -3.12 -m venv venv_py312
    if %ERRORLEVEL% NEQ 0 (
        echo Failed to create virtual environment.
        pause
        exit /b 1
    )
)

REM Activate the virtual environment and install required packages
echo Activating virtual environment and installing packages...
call venv_py312\Scripts\activate.bat

REM Install required packages
python -m pip install --upgrade pip
pip install torch torchvision
pip install facenet-pytorch
pip install fastapi uvicorn opencv-python pillow requests

echo Setup complete!
echo To start the service, run: run_pytorch_service.bat
pause 