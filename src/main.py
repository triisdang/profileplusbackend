from fastapi import FastAPI
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
@app.get("/postimage")
def postimage():
    return "wip"