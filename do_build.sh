#!/bin/bash
cp .env ./frontend/loopmeesters

cd ./backend
git restore .
git pull

cd ../frontend/loopmeesters
git restore .
git pull

cd ../../

docker compose build && docker compose up -d
