#Virtual Environment

virtualenv venv
venv\Scripts\activate

#Dependencies

pipenv install Flask
pipenv install flask_cors
pipenv install requests
pipenv install gunicorn

#Local Run

set FLASK_APP=time_series_server.py
python -m flask run

#Heroku deploy


https://time-series-server.herokuapp.com
