FROM python:3.8

EXPOSE 8080

WORKDIR /app

COPY requirements.txt /app
COPY app.py /app
COPY job_manager.py /app

RUN pip install -r requirements.txt

CMD python app.py