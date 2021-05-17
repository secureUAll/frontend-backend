echo "Removing database persistency folder..."
rm -r data/db

echo
echo "Removing old migrations..."
cd ../secureuall
./resetdata.sh

cd ../docker
echo
echo "Docker clean up has finished! Run the command below now:"
echo "$ docker-compose up -d --build"