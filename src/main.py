from fastapi import FastAPI, Header, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from supabase import create_client, Client
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import random
import json
from fastapi.middleware.cors import CORSMiddleware
import string

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASEURL")
SUPABASE_KEY = os.getenv("SUPABASEKEY")
JWT_SECRET = os.getenv("JwtSecret")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
app = FastAPI()
jsonget=json.loads

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def verify_token(authorization: str = Header(...)):
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid auth scheme")
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


def randomstuff():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


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
    randomticket = randomstuff()
    response = supabase.table('pendingDB').insert({
        "created_by": username,
        "url": url,
        "allowed": False,
        "ticket": randomticket
    }).execute()

    if response.data:
        return {"message": f'"success",ticket : {randomticket} , db: {response.data}'}
    return {"message": "Failed to insert data"}


@app.post("/ticket")
def ticketcheck(ticket: str = Header(...)):
    try:
        response = supabase.table('pendingDB').select("*").eq("ticket", ticket).single().execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"ticket not found or error: {str(e)}")


# LOGIN / SIGN UP / VERIFY SESSION #

@app.post("/signup")
def signup(email: str = Header(...), password: str = Header(...)):
    result = supabase.auth.sign_up({"email": email, "password": password})
    return result

@app.post("/login")
def login(email: str = Header(...), password: str = Header(...)):
    result = supabase.auth.sign_in_with_password({"email": email, "password": password})
    return result

@app.get("/session")
def protected_route(user=Depends(verify_token)):
    return {"message": "You are authenticated", "user": user}