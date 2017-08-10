# mibura.com
Mibura Company Website


How to run django server locally:
___

- Pull repository into a local folder
- Create a virtual environment with python 3.x

```
virtualenv -p python3 venv
```

- source into the virtualenv
- Install python packages using the requirements.txt file

```
cd *project folder*
pip install -r requirements.txt
```

- Run django database migrations

```
python manage.py migrate
```

- Create superuser

```
python manage.py createsuperuser
```

- Import test product database

```
python scripts/import_db.py
```

- Run development server

```
python manage.py runserver
```

# Front end development:

