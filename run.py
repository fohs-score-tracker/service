import uvicorn
import os
from dotenv import load_dotenv



load_dotenv()

if __name__ == "__main__":
    uvicorn.run("scoretracker:app", host=os.getenv("IP"), port=int(os.getenv("PORT")), reload=True)