cd ..\data

:: Create volume with data
docker volume create web_game_data

:: Create image with data
docker-compose build

:: Run container
docker-compose up

:: Remove created service
docker-compose down --rmi local

exit 0