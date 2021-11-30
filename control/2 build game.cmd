cd ..

:: Remove previous image and container
docker-compose down --rmi local

:: Build new one
docker-compose build

exit 0