echo "Removing database persistency folder..."
rm -r data/db

echo
echo "Removing old migrations..."
cd ../secureuall
./resetdata.sh

echo
echo "Building docker-compose..."
cd ../docker
docker-compose up -d --build