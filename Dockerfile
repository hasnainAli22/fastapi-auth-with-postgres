FROM python:3.9.7-alpine


WORKDIR /code

COPY requirements.txt ./

RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps


COPY . .
EXPOSE 8000
CMD [ "fastapi", "dev", "app/main.py", "--host",  "0.0.0.0", "--port", "8000" ]