# frontend-backend



## How to run locally?



### First time

1. Create a virtual environment on the project root;

```bash
$ virtualenv -p python venv
```

2. Initialize the venv;

```bash
$ source venv/bin/activate
```

3. Install the project requirements;

```bash
$ pip install -r requirements.txt
```

4. Apply the project migrations;

```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

5. Run the project in a local server

```bash
$ python manage.py runserver
```



### Next times

Just initialize the vend (step 2) and run the project (step 5).

```bash
$ source venv/bin/activate
$ python manage.py runserver
```

If changes to the mode were made, apply the project migrations (step 4) before running it.