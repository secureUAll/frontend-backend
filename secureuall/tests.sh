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

# Run tests
echo
echo "Running Django server..."
# python manage.py test --verbosity 2
coverage erase  # Remove any coverage data from previous runs
coverage run --omit=venv/*,*/migrations/*,*/tests/*,*/__init__.py,/usr/lib/*,/usr/local/*,/home/runner/* manage.py test --verbosity 2 # Run the full test suite
var=$?
coverage report -m
exit $var