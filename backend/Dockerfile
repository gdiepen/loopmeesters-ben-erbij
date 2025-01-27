FROM python:3.12-slim

WORKDIR /application

RUN pip install fastapi requests SQLAlchemy uvicorn

COPY . /application

RUN mkdir -p /application/sqlite_db/


CMD [ "uvicorn",  "--host", "0.0.0.0" , "app:app" ]


