from fastapi import FastAPI

app = FastAPI();

app.get("/")
def cheking():
     return {"message": "Hello, FastAPI on port 8080!"}