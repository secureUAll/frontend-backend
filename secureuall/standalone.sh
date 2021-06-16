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
python manage.py collectstatic --no-input

# Boot script
echo
echo "Running boot scripts..."
export DJANGO_SUPERUSERS='["secureuall@secureuall.pt"]'
python manage.py shell < boot_script.py
python manage.py dbshell < boot_db.sql

# Env vars
export EMAIL_HOST=exchange.ua.pt
export EMAIL_PORT=25
export EMAIL_USER=deti-vuln-mon@ua.pt
export EMAIL_PASSWORD=eGdgtY56eF#bve8AxeFe

# Run local server
echo
echo "Running Django server..."
python manage.py runserver
