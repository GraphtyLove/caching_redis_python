FROM python:3.10

RUN apt update -y
RUN apt install -y libgirepository1.0-dev
RUN pip install --upgrade pip

RUN mkdir /app
WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

CMD python3 -m uvicorn main:app --host 0.0.0.0 --port 8000