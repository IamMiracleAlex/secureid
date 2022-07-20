# Local Setup
1.  clone the repository
2.  create a virtual environment running python 3.8 (or above) - and activate it
    `python3 -m venv env` to create, and `source env/bin/activate` to activate (mac and linux) or `source env/Scripts/activate` (windows with `bash`)

3.  cd into the root of the django project (i.e the path containing manage.py)
4.  install requirements `pip install -r requirements.txt`
5.  Set up your environment variables using any credentials of your choice 
    but the names of the variable must match those contained in mysite/settings.py. Create an `.env` file and paste in the contents of `env.sample` with the correct credentials
6.  Create a local postgres instance (or use an existing one)
7.  Set your DB and make sure the environment variable names are consistent with (mysite/settings.py)
8.  run `python manage.py migrate` to create database tables
9.  run `python manage.py createsuperuser` to create a superuser(An initial user that has access to the admin site)
11. run `python manage.py runserver` to start the development server

The application should now be running on port 8000 (localhost:8000)
admin site available at localhost:8000

Goto localhost:8000/docs/ for documentation




