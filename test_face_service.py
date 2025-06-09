import requests
import time

def test_face_service():
    """Test if the face recognition service is running"""
    try:
        response = requests.get("http://localhost:8003/", timeout=5)
        if response.status_code == 200:
            print("Face recognition service is running!")
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"Service responded with status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to face recognition service: {e}")
        return False

if __name__ == "__main__":
    print("Testing connection to face recognition service...")
    for attempt in range(3):
        if test_face_service():
            break
        else:
            print(f"Attempt {attempt+1} failed. Retrying in 2 seconds...")
            time.sleep(2) 