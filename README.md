# Project 2

## Get Started

### Create a Python virtual environment

```bash
python -m venv .venv
```

### Activate the virtual environment

```bash
source .venv/bin/activate
```

### Install the dependencies

```bash
pip install -r requirements.txt
```

### Start MongoDB Locally

### Create tables in MongoDB

```bash
python manage.py migrate
```

### Import the data

```bash
sh imports.sh
```

### Start the development server

```bash
python manage.py runserver
```

## Contribute

After making updates to models, run the following command to generate the migration files:

```bash
python manage.py makemigrations
python manage.py migrate
```
