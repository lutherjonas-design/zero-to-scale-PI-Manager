To setup the env.:
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
To run:
uvicorn main:app --reload
python client.py "hello"