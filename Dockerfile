#https://medium.com/firebase-developers/hosting-flask-servers-on-firebase-from-scratch-c97cfb204579
#https://cloud.google.com

# 1 
FROM python:3.7

# 2
RUN pip install Flask gunicorn

# 3
WORKDIR /

# 4
ENV PORT 8080

# 5
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app