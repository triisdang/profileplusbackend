clear
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
cd src
uvicorn main:app --reload
