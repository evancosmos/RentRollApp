#https://medium.com/firebase-developers/hosting-flask-servers-on-firebase-from-scratch-c97cfb204579
#https://cloud.google.com
#gcloud builds submit --tag gcr.io/rent-roll-webapp/flask-fire && gcloud beta run deploy --image gcr.io/rent-roll-webapp/flask-fire && firebase deploy

# 1 
FROM python:3.10-slim

COPY ./ /app
WORKDIR /app

RUN pip3 install --no-cache-dir -r requirements.txt

ENV PORT 8080

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 main:app