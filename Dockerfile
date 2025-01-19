FROM python:3.12-slim

WORKDIR /application

RUN pip install fastapi requests SQLAlchemy uvicorn

COPY . /application

RUN mkdir /application/sqlite_db/


CMD [ "uvicorn",  "app:app" ]


