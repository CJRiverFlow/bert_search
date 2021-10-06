from python:3.7

RUN apt-get update -y 

WORKDIR /app

COPY /api /app

COPY requirements.txt /app

RUN pip3 install -r requirements.txt

CMD python main.py