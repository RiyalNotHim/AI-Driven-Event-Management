import subprocess
import time
import webbrowser

# Start FastAPI backend
backend_process = subprocess.Popen(["uvicorn", "chatbot:app", "--host", "127.0.0.1", "--port", "8000", "--reload"])

# Wait a few seconds to ensure the backend starts
time.sleep(3)

# Open the frontend in a browser
webbrowser.open("file:///C:/Users/Athashree/Desktop/super/index.html")  # Update this path to your actual index.html location

# Keep the script running so the backend doesn't close
try:
    backend_process.wait()
except KeyboardInterrupt:
    backend_process.terminate()
