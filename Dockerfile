FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python3.8 python3-dev  build-essential pip gunicorn
RUN pip install --upgrade setuptools
RUN pip install ez_setup
COPY . /app
WORKDIR /app
RUN pip install -r /app/requirements.txt
RUN echo "from django.contrib.auth import get_user_model; \
          User = get_user_model();  \
          User.objects.create_superuser('admin', 'emial@gmail.com', 'password')" | python3 manage.py shell
CMD [ "python3", "manage.py", "migrate" ]
CMD [ "python3", "manage.py", "collectstatic" ]
CMD [ "gunicorn", "wsgi:application", "-b", "0.0.0.0:8000"]
