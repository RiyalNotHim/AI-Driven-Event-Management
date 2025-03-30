import subprocess
import time
import webbrowser

# Start FastAPI backend
backend_process = subprocess.Popen(["uvicorn", "main:app", "--reload"])

# Wait for backend to start
time.sleep(3)

# Open frontend in browser
webbrowser.open(r"D:\PROGRAMMING\Event Managament\frontend\homepage\post sentiment analysis\senti\index.html")  # Replace with actual file path
