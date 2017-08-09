# precond ubuntu

sudo apt install libffi-dev
sudo apt install libncurses5-dev

# utility ubuntu

sudo apt install jq


# interactive 


curl -H post 'http://s1.wolfslab.local.wolfspool.at:8000/notes' | jq '.' | less

# Falcon-REST-API-Pattern
Massively scalable RESTFul API design with Falcon and PyPy

Please be sure that your virtual environment is faconenv PyPy interpreter.

`$ source falconenv/bin/activate`

Then run 

`(falconenv)$ pip install -r requirements.txt`

Then serve app using gunicorn

`(falconenv)$ gunicorn app:api`

Now visit http://localhost:8000/notes/

to fetch notes using GET request.
