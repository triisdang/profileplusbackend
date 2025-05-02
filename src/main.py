from fastapi import FastAPI, Header
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from supabase import create_client, Client
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASEURL")
SUPABASE_KEY = os.getenv("SUPABASEKEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
app = FastAPI()

class User(BaseModel):
    name: str

@app.get("/favicon.ico")
def favicon():
    return FileResponse("stuff/favicon.ico")

@app.get("/")
def test():
    response = supabase.table("test").select("*").execute()
    return response.data

@app.post("/postimage")
def postimage(url: str = Header(...), username: str = Header(...)):
    response = supabase.table('pendingDB').insert({
        "created_by": username,
        "url": url
    }).execute()

    if response.data:
        return {"message": f"success, db: {response.data}"}
    else:
        return {"message": "Failed to insert data"}
