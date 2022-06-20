from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def welcome():
  x = {"message": "Warriors will beat the celtics tonight"}
  return x
