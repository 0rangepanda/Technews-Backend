

## Set up Project
  install git and nginx:
  > sudo yum install git

  > sudo yum install nginx

  create python virtual environment:
  > sudo pip install virtualenv

  > virtualenv -p python2.7 project
  #make sure use version 2.7, 2.7.10 is prefered

  > source bin/activate

  get source code from githab:
    (If using AWS, install git first:
  > yum install git

  > git clone https://github.com/0rangepanda/Technews-Backend.git


  Install python packages:
  > pip install -r requirements.txt

  Run server:
  > python server.py

  Now you can access it on localhost:5000 via local machine


## Gunicorn
To deploy as a flask web application using gunicorn:
  Install gunicorn:
  > pip install gunicorn

  Run app container and save pid:
  > gunicorn server:app -p server.pid -D

  > cat server.pid
  #this will store the pid of gunicorn in case to stop it

  > kill `cat server.pid`


## Nginx
  stop apache server firstly:
  > sudo apachectl stop

  Set nginx configure file nginx.conf:

    # Handle requests to exploreflask.com on port 80
    server {
            listen 80;
            server_name localhost;

            # Handle all locations
            location / {
                    # Pass the request to Gunicorn
                    proxy_pass http://127.0.0.1:8000;

                    # Set some HTTP headers so that our app knows where the request really came from
                    proxy_set_header Host $host;
                    proxy_set_header X-Real-IP $remote_addr;
                    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            }
    }

  Then start nginx server:
  > sudo nginx



## Note:


#### 1. Replacebale files:
  In data folder:
  - stopword - the stop word list file, which will be used by rake
  - techlist - the tech word list file, which will be used to filter the result of mapreduce job
  - My ProjectXXX.json - authentification file for google big query project
  - requirements.txt - If install any new packages -> In folder data, run:
    > pip freeze > requirements.txt
