clear
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
cd src
pip install -r requirements.txt
clear
echo "starting server..."
uvicorn main:app --reload
