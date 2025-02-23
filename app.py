import os
import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "FastAPI is running on Render!"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Default port for Render
    uvicorn.run(app, host="0.0.0.0", port=port)
