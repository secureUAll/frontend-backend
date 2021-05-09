# frontend-backend



- [SSL Certificate for deploy environment](SSL-Certificate-for-deploy-environment)



## SSL Certificate for deploy environment

On deploy environment, nginx runs with a certificate issued by a custom CA. For the browser to trust it, it must be installed first. See how on [ssl/README.md](ssl/README.md).



## Authentication and database

The method for authentication in production is the UA IdP. However, as it redirects to the server URL, it is not suitable for testing and development. To allow local testing it was developed a simple authentication method that resumes to introducing the email address.

The database is a dockerized PostgreSQL database. However, when someone only needs to test the interface without any other components, running Docker is not an efficient approach and the Django  lightweight development Web server on the local machine is a better option.

To allow the combination of all this approaches Django reads the value of `RUNNING_MODE` environmental variable.

| Authentication \ Database | Postgres                | SQLite  |
| ------------------------- | ----------------------- | ------- |
| IdP                       | RUNNING_MODE=production | -       |
| Local authentication      | RUNNING_MODE=docker     | Default |

 



## How to run locally?

> This tutorial only runs the frontend, without integration with other services like the database or nginx. To run it with those services, go to [docker/README.md](docker/README.md).



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