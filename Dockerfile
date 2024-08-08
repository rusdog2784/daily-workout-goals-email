FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY email_body.html .
COPY gmail.py .
COPY main.py .

CMD ["python", "main.py"]
