cd ..

:: Remove image and container
docker-compose down --rmi local

:: Remove volume
docker volume rm web_game_data

exit 0