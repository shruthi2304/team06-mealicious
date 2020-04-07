#Go to the folder you have cloned into
cd <your_file_path>/team06-mealicious

#Run the below commands

#To set the application configuration 
set FLASK_APP=mealicious.py
set FLASK_DEBUG=1 #Only for Debug Purpose

#After you set up postgres, create a database called "Mealicious" and run the following commands
flask db migrate -m "Initial Database creation"
flask db upgrade

#To install all the dependencies
pip install -r requirements.txt

#To run the application
flask run

#Below is the output of the "flask run" and open your browser to "http://127.0.0.1:5000/"
################################
 * Serving Flask app "mealicious.py" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 157-254-369
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
################################

