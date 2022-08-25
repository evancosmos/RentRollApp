#https://medium.com/firebase-developers/hosting-flask-servers-on-firebase-from-scratch-c97cfb204579
#https://cloud.google.com

# 1 
FROM python:3.10-slim

# 2
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# 3
RUN pip install --no-cache-dir -r requirements.txt

# 4
ENV PORT 8080

# 5
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app