# Create new venv
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

# Reset data 
echo
echo "Reset data..."
./resetdata.sh

# Reinstall Django (to avoid compatibility issues)
echo
echo "Reinstalling Django (to avoid compatibility issues)"
pip install --upgrade --force-reinstall Django

# Set up Django
echo
echo "Django set up..."
python manage.py makemigrations
python manage.py migrate
export DJANGO_SUPERUSER_PASSWORD=aJAG72Jas
export DJANGO_SUPERUSER_USERNAME=secureuall
export DJANGO_SUPERUSER_EMAIL=secureuall@secureuall.pt
python manage.py createsuperuser --noinput
echo -e "from login.models import User\nimport os\nu=User.objects.get(username=os.environ.get('DJANGO_SUPERUSER_USERNAME', ''))\nu.is_admin=True\nu.save()\nprint(f\"Superuser ({u.username}) with admin status created! :)\")" | python manage.py shell
python manage.py collectstatic --no-input

# Run local server
echo
echo "Running Django server..."
python manage.py runserver
