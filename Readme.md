# Local Setup
1.  clone the repository
2.  create a virtual environment running python 3.8 (or above) - and activate it
    `python3 -m venv env` to create, and `source env/bin/activate` to activate (mac and linux) or `source env/Scripts/activate` (windows with `bash`)

3.  cd into the root of the django project (i.e the path containing manage.py)
4.  install requirements `pip install -r requirements.txt`
5.  Set up your environment variables using any credentials of your choice 
    but the names of the variable must match those contained in mirapayments/settings.py. Create an `.env` file and paste in the contents of `env.sample` with the correct credentials
6.  Create a local postgres instance (or use an existing one)
7.  Set your DB and make sure the environment variable names are consistent with (mirapayments/settings.py)
8.  run `python manage.py migrate` to create database tables
9.  run `python manage.py createsuperuser` to create a superuser(An initial user that has access to the admin site)
11. run `python manage.py runserver` to start the development server

The application should now be running on port 8000 (localhost:8000)
admin site available at localhost:8000

# Development:
1. If your update requires a third party library to function, endeavour to update the `requirements.txt` file and add a comment of what the package does. (**DO NOT RUN** `pip freeze > requirements.txt`)
 Ensure only needed libraries are added and remove a library no longer in use
    from requirements to avoid unnecsaary dependencies

2. If your update requires change in the database, endeavour to pull from the origin to effect any exisiting migrations before creating your own migrations. Generate migrations locally before pushing
    with `python manage.py makemigrations`. Test applying migrations locally and fix possible errors.

3. Provide docstrings and comments that adequately describes your operation/aim/usage in the code base

4. Write tests for all your implementations

5. When creating a model field that has choices, use this convention
- Save choices as class attributes 
-  Choices should be title cased
```
class ModelName(models.Model):

    FIRST = 'First'
    SECOND = 'Second'
    THIRD = 'Third'
  
    FIELD_CHOICES = (
        (FIRST, FIRST),
        (SECOND, SECOND),
        (THIRD, THIRD),
    )
    field_name = models.CharField(choices=FIELD_CHOICES, )
```

6. Some `classes`, `files` and `functions` are deemed **PROCTECTED**. Do **NOT** modify them without proper consultation, else your PR won't be merged.

7. When defining a foreign key, one to one or many to many field to a model, use the example below to avoid circular imports error. This would also allow the application to scale seamlessly.

`field_name = models.ForeignKey('module.ModelName', ...)`

8. Make a pull request. Do **NOT** push to the `master` branch.

9. Because we customized the API response, please do not use `data` as a field_name on a model or serializer field.




# Authentication
 Json Web Tokens to handle authentication



