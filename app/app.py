from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def welcome():
  x = {"message": "Warriors did win"}
  return x
