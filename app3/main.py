from fastapi import FastAPI

app = FastAPI()


student = [
    {"id": 304, "name": "Wongseuang Loachai", "student_id": "681310304"},
    {"id": 499, "name": "Rachta Phonphaem", "student_id": "681310499"},
    {"id": 300, "name": "Thanaporn Saengkaew", "student_id": "681310300"},
    {"id": 398, "name": "Jirapat Boonyahutanoon", "student_id": "681310498"},
    {"id": 301, "name": "Teerawut Tadput", "student_id": "681310301"},
]

@app.get("/")
def home():
    return {"message": "Welcome to Class App3"}


@app.get("/students")
def get_students():
    return student


@app.get("/student/{id}")
def get_student(id: str):
    for s in student:
        if s["id"] == id:
            return s
    return {"error": "student not found"}