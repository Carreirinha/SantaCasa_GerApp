
FROM python:latest

COPY banco_flask.py . ./
WORKDIR /app
RUN pip install SQLAlchemy
RUN pip install flask

CMD [ "python", "./banco_flask.py" ]
