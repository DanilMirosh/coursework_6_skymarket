# start from an official message
FROM python:3.10-slim

# set work directory
WORKDIR /code

# install dependencies
RUN pip install --upgrade pip
RUN pip install django psycopg2-binary
RUN pip install drf-spectacular django-cors-headers djangorestframework djoser djangorestframework-simplejwt pillow
RUN pip install gunicorn

# copy project
COPY . .

# expose the port 8000
EXPOSE 8000

# define the command to run when starting the container
CMD ["gunicorn", "--bind", ":8000", "backend_django.wsgi:application"]
