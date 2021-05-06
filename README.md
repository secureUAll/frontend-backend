# frontend-backend



## Table of contents

- [How to run?](#How-to-run?) 
- [Authentication and database](#Authentication-and-database)
- [Sample data](#sample-data)
- [Reset data](#reset-data)



## How to run?

### Standalone

To run Django with a local SQLite database and no integration with external services, just run `python manage.py runserver`.

To ease the process of set up (migrations, collect static files, ...) and populate the database with sample data, just run the [`standalone.sh`](standalone.sh) script. It will execute all the necessary commands, since starting the virtual environment to running the local server.

```bash
$ chmod +x standalone.sh
$ ./standalone.sh
```



### Docker

The integration of Django with other services is handled by Docker, that deploys all of the necessary stuff in containers and creates the connections needed. To run Django with Docker see the tutorial al [docker/README.md](docker/README.md).



## Authentication and database

The method for authentication in production is the UA IdP. However, as it redirects to the server URL, it is not suitable for testing and development. To allow local testing it was developed a simple authentication method that resumes to introducing the email address.

The database is a dockerized PostgreSQL database. However, when someone only needs to test the interface without any other components, running Docker is not an efficient approach and the Django  lightweight development Web server on the local machine is a better option.

To allow the combination of all this approaches Django reads the value of `RUNNING_MODE` environmental variable.

| Authentication \ Database | Postgres                | SQLite  |
| ------------------------- | ----------------------- | ------- |
| IdP                       | RUNNING_MODE=production | -       |
| Local authentication      | RUNNING_MODE=docker     | Default |



## Sample data

Sample data is stored at `fixtures/fixture.json` folder inside every app. 

To load this data, just run the command below. Django will look for all `fixtures` folders inside every app and map that data to the database.

> This process is done by [`standalone.sh`](standalone.sh) by default.

```bash
$ python manage.py loaddata fixture
```

New data can be added through the Django admin (/admin). To map it to the files inside the `fixtures` folder, just run the command below.

```bash
# Save tables for app workers in workers/fixtures/fixture.json
$ python manage.py dumpdata workers --output workers/fixtures/fixture.json
```



## Reset data

To reset the data and remove the migrations, just run [`resetdata.sh`](resetdata.sh) script.

```bash
$ chmod +x ./resetdata.sh
$ ./resetdata.sh
```

