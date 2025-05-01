from fastapi import FastAPI
from supabase import create_client, Client
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv() 

SUPABASE_URL = os.getenv("SUPABASEURL")
SUPABASE_KEY = os.getenv("SUPABASEKEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
app = FastAPI()

@app.get("/test")
def test():
    supabase.table("test").insert({"name": "fucker"}).execute()
