To setup the env.:
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
To run:
Server (run from project root):
source .venv/bin/activate
uvicorn manager.main:app --reload
cli:
python client.py "hello"

I need to create a programm, to manage my build process for my PI. I don't know if I should invest the time in it now or later. The funtionality that is planned:
1. run as a background task and check for changes in the depositories in a folder (/mnt/dev_storage/repos/)
2. if change, look at the service.yml file, if it exists go on with the process decided for that (which dev tags and if it should sleep and what is it)
3. create a copy, because this is a bare repo in a dev_storage/apps and move the secrets into there.
4. handle collisions and fast pushes, i.e. queue and if we have a later push, we build for that and can ignore the one before.

Right now validator and Functions