clear
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
cd src
source venv/bin/activate
uvicorn main:app --reload
