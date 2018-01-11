# flask-mvvm-r
### MVVM-R(Model-View-ViewModel-Router) patern for large flask applications
#### This project uses following flask tool-kits:
- Flask-WTF(for secure forms)
- Flask-Login(for seure sessions)
- Flask-SQLAlchemy(for db integration)
- Flask-Bootstrap(beautify)

## How to run

### Requirements
- Tested with python 3.5 or upper
- pip3
- virtualenv

### Setup

- go to project directory and ``` virtualenv --python=python3 venv ``` than ```source venv/bin/activate```
- be sure that you are in virtualenvironment ```(venv)user@machine: dir ``` in terminal.
- after that ```pip install -r requirements.txt``` 
- finally up the gunicorn ```gunicorn --bind 127.0.0.1:5000 runserver:app```
- That's it now go to: (http://127.0.0.1:5000)
