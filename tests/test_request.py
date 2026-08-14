import requests
import time
import subprocess
import os

python_exe = r"C:\Users\504508\PythonProject\PythonChatBot\ai_petcare_Assistant\venv\Scripts\python.exe"
proc = subprocess.Popen(
    [python_exe, "-m", "uvicorn", "app.main:app", "--port", "8000"], 
    cwd="C:\\Users\\504508\\PythonProject\\PythonChatBot\\ai_petcare_Assistant"
)
time.sleep(5)

try:
    response = requests.post(
        "http://localhost:8000/api/v1/chat",
        json={
            "user_id": "USER-1001",
            "message": "Find a clinics near me in San Francisco for Max"
        }
    )
    print("Status Code:", response.status_code)
    print("Response JSON:", response.text)
finally:
    proc.terminate()
