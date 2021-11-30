FROM ubuntu

# Update apt-get
RUN apt-get clean && apt-get update && apt-get install -y locales

# Set UTF-8
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# Agh!?
RUN apt-get install nano

COPY . .

# Fill the volume with a game data
CMD ["cp", "my_data/game_routes.json", "data/game_routes.json"]
