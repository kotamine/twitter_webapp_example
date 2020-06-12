# Twitter Webapp Example 

This site is a simple web application of **Twitter data streaming and analysis**, powered by **Twitter API**, **Python**, **Flask**, and **JavaScript**.

[Live app on AWS](http://ec2-3-128-18-23.us-east-2.compute.amazonaws.com/)

This project is based on <a href="https://www.pythonforengineers.com/build-a-twitter-analytics-app-using-python/">an online tutorial</a> with some modifications. 

Additionally, the following sites were useful:
- Flask app auto-update with JavaScript https://www.reddit.com/r/flask/comments/esfcyq/update_site_live_with_mysql_data/
- JavaScript learning https://playcode.io/
- Docker into https://runnable.com/docker/python/dockerize-your-flask-application
- Docker using a persistent data in volume https://docs.docker.com/storage/volumes/
- Docker CMD vs ENTRYPOINT https://aws.amazon.com/blogs/opensource/demystifying-entrypoint-cmd-docker/
- Deployment in AWS https://realpython.com/twitter-bot-python-tweepy/



## Notes to myself

### Run locally
    python flask3.py
    python trendstream4.py

### Run flask app with docker, using local twitter_data.db 
    docker image build . -t webapp
    docker run -p 5000:5000 webapp 
    python trendstream4.py

### Run flask app and Twitter data gathering with docker-compose, using a shared docker volume
    docker-compose build
    docker-compose up

### Deploy on Amazon AWS
One way to do it is:

    docker-compose build
Upload docker images to AWS EC2 instances and modify docker-compose.yaml for instantiating images and run

	docker-compose up





