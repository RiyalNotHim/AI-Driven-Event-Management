import openai
from pymongo import MongoClient

client = MongoClient("mongodb+srv://bogeprathmesh:secure12345@cluster0.iwmcgzx.mongodb.net/eventDB?retryWrites=true&w=majority&appName=Cluster0")
db = client["eventDB"]  # Ensure the database name matches
students_collection = db["formdatas"]
tasks_collection = db["tasks"]

# OpenAI API Key (Replace with your key)
openai.api_key = "AIzaSyA4TIHZ_ezXBTJ8s9VFzWpHH4S8zv5JGlE"

class AITaskAllocator:
    def __init__(self):
        self.tasks = list(tasks_collection.find({}, {"_id": 0, "task": 1}))
        self.students = list(students_collection.find({}, {"_id": 0}))

    def generate_task_steps(assigned_task):
        if not assigned_task:  # Check if assigned_task is empty or None
            raise ValueError("Assigned task is empty. Cannot generate prompt.")

        prompt = f"Generate a step-by-step guide for {assigned_task} in an event management scenario."

        response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert event planner."},
            {"role": "user", "content": prompt}
        ]
    )

        # Extract generated response
        return [step.strip() for step in steps_list if step.strip()]  # Remove empty lines

    def assign_task(self, student):
        """ Assign task based on experience and generate AI-based steps """
        experience = student.get("experience", "General").lower()

        # AI-based task matching categories
        task_mapping = {
            "technical": "Stage & Technical Setup",
            "management": "Venue Selection & Booking",
            "marketing": "Marketing & Promotion Strategy",
            "logistics": "Food & Beverage Management",
            "volunteering": "Volunteer Recruitment & Training",
        }

        assigned_task = task_mapping.get(experience, "General Event Support")

        # 🔥 AI-generated Steps
        task_steps = self.generate_task_steps(assigned_task)

        return {
            "task": assigned_task,
            "steps": task_steps
        }
