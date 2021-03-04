FROM python:3.8.3-alpine

WORKDIR /code
COPY requirements.txt /code/

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./entrypoint.sh /code/
RUN chmod +x entrypoint.sh

# copy project
COPY . /code/

ENTRYPOINT ["/code/entrypoint.sh"]