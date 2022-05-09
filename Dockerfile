FROM python:3.8-alpine

WORKDIR /usr/app

RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev

COPY . .

RUN pip install -r requirements.txt --upgrade pip

EXPOSE 5000

CMD ["python", "app.py"]