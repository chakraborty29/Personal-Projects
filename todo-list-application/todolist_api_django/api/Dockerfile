# pull official base image
FROM python:3.8

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONNUNBUFFERED 1

# install psycopg2 dependencies
RUN apt-get -y update && apt-get -y upgrade && \
    apt-get install -y bash git libpq-dev \
    postgresql-client \
    gcc \
    python3-dev \
    musl-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r /usr/src/app/requirements.txt

EXPOSE 8000

COPY ./entrypoint.prod.sh /usr/src/app/entrypoint.sh
# RUN sed -i 's/\r$//g' /workspace/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# copy project 
COPY . /usr/src/app/

# run entrypoint.prod.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]