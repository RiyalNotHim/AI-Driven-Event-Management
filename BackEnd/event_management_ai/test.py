from ai_allocator import predict_task

# Test cases
tests = [
    (1, 15),  # Tech event, 15 students
    (1, 40),  # Tech event, 40 students
    (2, 10),  # Cultural event, 10 students
    (2, 50)   # Cultural event, 50 students
]

# Run predictions
for event_type, students in tests:
    print(f"Event Type: {event_type}, Students: {students} → Assigned Task: {predict_task(event_type, students)}")
