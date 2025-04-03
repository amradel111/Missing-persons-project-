# AI-Based Missing Persons Facial Recognition System

A Django-based web application that helps find missing people in public places using face recognition technology to analyze uploaded video footage.

## Project Overview

This system allows users to:
- Upload photos of missing persons
- Upload or link to video footage (recorded or live)
- Search through the footage using AI-powered facial recognition
- Track potential matches in real-time
- Receive notifications when matches are found

## Current Features
- User authentication (login/signup)
- More features coming soon...

## Project Structure
```
missing_persons_project/
├── config/             # Project configuration
├── core_app/          # Core functionality
├── user_auth/         # User authentication
├── search_manager/    # Search functionality
├── video_processor/   # Video processing and face recognition
├── static/           # Static files
├── media/           # User-uploaded files
└── templates/       # HTML templates
```

## Setup and Installation

1. Clone the repository:
```bash
git clone https://github.com/amradel111/ai-based-missing-persons-facial-recognition.git
cd ai-based-missing-persons-facial-recognition
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
cd missing_persons_project
python manage.py migrate
```

5. Start the development server:
```bash
python manage.py runserver
```

## Contributing
This is a university project currently under development.

## License
This project is licensed under the MIT License. 