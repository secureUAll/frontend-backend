#!/bin/bash

RETRIES=40

echo "Waiting for db..."
until PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U $DB_USER -p $DB_PORT -d $DB_NAME -c "select 1" > /dev/null 2>&1 || [ $RETRIES -eq 0 ]; do
  echo "Waiting for postgres server, $((RETRIES--)) remaining attempts..."
  sleep 5
done

echo "Connected to database!."

echo
echo "Removing old migrations..."
./resetdata.sh

echo
echo "Making new migrations..."
python3 manage.py makemigrations
python3 manage.py migrate

echo
echo "Creating createsuperusers..."
python3 manage.py createsuperuser --noinput
echo -e "from login.models import User\nimport os\nimport json\nenv = os.getenv('DJANGO_SUPERUSERS')\nprint('Got env', env)\nif not env: \n\texit()\nemails = json.loads(env)\nfor e in emails:\n\tu = User.objects.create_user(username=e, email=e)\n\tu.is_admin=True\n\tu.save()\n\tprint(f'Superuser ({e}) with admin status created! :)')\n" | python manage.py shell

echo
echo "Collecting static..."
python3 manage.py collectstatic --no-input

# Boot script
echo
echo "Running boot scripts..."
python manage.py shell < boot_script.py
python manage.py dbshell < boot_db.sql

echo
echo "All set! :) Starting server on port 9000..."
gunicorn --bind 0.0.0.0:9000 secureuall.wsgi:application --log-level debug --log-file /var/log/frontend_gunicorn.log

