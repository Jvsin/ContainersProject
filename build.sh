#!/bin/bash

docker-compose down
docker rmi frontend connection api

docker build -t frontend ./front
docker build -t connection ./connection
docker build -t api ./api

docker-compose up -d