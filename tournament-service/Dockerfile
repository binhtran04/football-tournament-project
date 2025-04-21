FROM python:3.11-alpine

WORKDIR /app
COPY app.py .

RUN pip install pyzmq

CMD ["python", "app.py"]
