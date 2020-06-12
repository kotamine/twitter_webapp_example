
# Run from docker-compose, using a shared docker volume
docker-compose build
docker-compose up

# Run from docker, using local twitter_data.db 
docker image build . -t webapp
docker run -p 5000:5000 webapp 
python trendstream4.py

# Run locally
python flask3.py
python trendstream4.py


