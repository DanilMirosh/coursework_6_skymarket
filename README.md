# SkyPro.Python course
## Skymarket - avito-like ads site

### Implementation

1. Backend: django restframework
2. Database: postgresql 
3. Backend-server: gunicorn
4. Web-server: nginx (from docker image)
5. Frontend: react (was provided)

frontend available at: localhost:3000  
backend at: localhost:8000

### How to launch project locally using docker for every service

Project is set to start all necessary docker containers and populate database from single command.  
Just perform the following command: `docker-compose up --build -d`

### How to launch project locally using docker only for db and front

If for some reason you want to launch django manually:

1. Perform the following commands in succession:  
`cd deploy`  
`docker-compose up --build -d` to start frontend and db
`cd ../backend_django`  
`./manage.py migrate`  
`./manage.py loadall`  
`django-admin runserver` to start backend


