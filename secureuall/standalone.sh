# Set up venv
DIR="./venv"
if [ ! -d "$DIR" ]; then
  # If venv does not exist, create it
  echo "venv does not exist, creating it..."
  virtualenv -p python venv
  source venv/bin/activate
  pip install -r requirements.txt
else
  # Activate venv
  source venv/bin/activate
fi
# Set up Django
python manage.py makemigrations
python manage.py migrate
export DJANGO_SUPERUSER_PASSWORD=aJAG72Jas
export DJANGO_SUPERUSER_USERNAME=secureuall
export DJANGO_SUPERUSER_EMAIL=secureuall@secureuall.pt
python manage.py createsuperuser --noinput
python manage.py collectstatic --no-input
# Load sample data
python manage.py loaddata fixture
# Run local server
python manage.py runserver
