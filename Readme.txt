pip install -r requirements.txt
set FLASK_APP=mealicious.py
set FLASK_DEBUG=1 #Only for Debug Purpose

flask db migrate -m "Initial Database creation"
flask db upgrade

