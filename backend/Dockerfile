FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Utils
RUN apt-get update
RUN apt-get install -y software-properties-common
RUN apt-get install -y vim
RUN apt-get install -y openssh-client openssh-server
RUN apt-get install -y iputils-ping

COPY . .

CMD [ "flask", "run" ]