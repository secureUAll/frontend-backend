
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

# Set up Django
echo
echo "Django set up..."
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input

# Run local server
echo
echo "Running Django server..."
python manage.py test --verbosity 2
exit $?