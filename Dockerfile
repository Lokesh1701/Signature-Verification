From python:3.8

FROM jjanzic/docker-python3-opencv

ENV PYTHONUNBUFFERED 1

COPY ./signVerify signVerify

WORKDIR signVerify

RUN pip install -U pip

RUN pip install -r requirements.txt -U

RUN python manage.py makemigrations verifyApp

RUN python manage.py migrate

CMD ["python","manage.py","runserver", "0.0.0.0:8000"]

