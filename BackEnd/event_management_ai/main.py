from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
import uvicorn
from urllib.parse import unquote
from fastapi.middleware.cors import CORSMiddleware
import random
# 🚀 Connect to MongoDB
client = MongoClient("mongodb+srv://bogeprathmesh:secure12345@cluster0.iwmcgzx.mongodb.net/eventDB?retryWrites=true&w=majority&appName=Cluster0")

db = client["eventDB"]

# ✅ Collections
students_collection = db["formdatas"]  # Contains student details
tasks_collection = db["tasks"]  # Contains different tasks

# 🔥 Initialize FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (or specify your frontend URL)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def home():
    return {"message": "AI Event Task Manager is Running 🚀"}

# ✅ Fetch all students
@app.get("/students/")
async def get_students():
    students = list(students_collection.find({}, {"_id": 0, "name": 1, "age": 1}))  # Fetching only name and age
    if not students:
        raise HTTPException(status_code=404, detail="No students found in DB")
    return students

# ✅ Fetch all available tasks
@app.get("/tasks/")
async def get_tasks():
    tasks = list(tasks_collection.find({}, {"_id": 0}))
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found in DB")
    return {"tasks": tasks}

# ✅ Fetch events & participants
@app.get("/events/")
async def get_events():
    events = students_collection.distinct("event")
    if not events:
        raise HTTPException(status_code=404, detail="No events found")
    return {"events": events}

# ✅ Fetch participants of a specific event
@app.get("/events/{event_name}")
async def get_event_participants(event_name: str):
    event_name = unquote(event_name)  # Decode URL spaces
    participants = list(students_collection.find({"event": event_name}, {"_id": 0, "name": 1}))
    
    if not participants:
        raise HTTPException(status_code=404, detail=f"No participants found for event '{event_name}'")
    
    return {"event": event_name, "participants": participants}

# ✅ AI-based Task Assignment
@app.get("/assign-tasks/{student_name}")
async def assign_task(student_name: str):
    student_name = unquote(student_name)

    # 🔍 Find student in DB
    student = students_collection.find_one({"name": student_name}, {"_id": 0})
    if not student:
        raise HTTPException(status_code=404, detail=f"Student '{student_name}' not found")

    # 🔥 Fetch all tasks
    all_tasks = list(tasks_collection.find({}, {"_id": 0}))
    if not all_tasks:
        raise HTTPException(status_code=500, detail="No tasks available for assignment")

    # 🤖 AI-based task allocation (random for now, can be improved)
    assigned_task = random.choice(all_tasks)

    return {
        "message": f"Task '{assigned_task['task']}' assigned to {student_name}",
        "experience": student.get("experience", "General"),
        "steps": assigned_task.get("steps", "Follow the standard procedure")
    }

# 🚀 Run FastAPI
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
