# mibura.com
Mibura Company Website

___
# Development

### How to run django server locally:

Pull repository into a local folder
Create a virtual environment with python 3.5.x

*Must use a version of python above 3.5*

```
virtualenv -p python3 venv
```

source into the virtualenv
Install python packages using the requirements.txt file

```
cd *project folder*
pip install -r requirements.txt
```

Run django database migrations

```
python manage.py migrate
```

Create superuser

```
python manage.py createsuperuser
```

Import Database data
*Run the following commands in order as shown to prevent errors*

```
bash scripts/loaddata.sh

```

*optional*
Load Product data from excel files in scripts/files/products/*.xlxs *instead* of the above Products.txt database dump file.  *This will not include product release dates, the database dump will*
```
python scripts/import_db.py
```

Run development server

```
python manage.py runserver
```

###  Front end development:

cd into the vuejs folder
```
cd static/js/sss
```

Install npm libraries
```
npm install .
```

run development server
```
npm run dev
```

View the site at http://localhost:8080

To view the site from within the django server, or in a production environment on port 80, run the build script

```
npm run build
```

This will create the JS bundle file that the Django page at /support/purchase uses, and can now be viewed on the django server at http://localhost:8000/support/purchase, or on the staging or production server.
