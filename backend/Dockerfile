FROM python:3.11.2-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app

CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0"]