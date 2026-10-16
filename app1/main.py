from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello():
    return{"messge": "Hello, World!"}

@app.get("/about")
def about():
    return{"app": "My First API app", "version": "1.0.0"}

@app.get("/info")
def info():
    return{"Name": "TEERAWUT TADPET", "ID": "681310301"}