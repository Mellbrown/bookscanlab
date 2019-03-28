#!/bin/bash

sudo docker stop bookscanlab
sudo docker rm bookscanlab

#cd ./front
#yarn build
#cd ../

sudo docker build -t bookscanlab .
sudo docker run -d --name bookscanlab -p 80:80 bookscanlab

docker rmi $(docker images -f "dangling=true" -q)
#
#address=`sudo docker inspect -f {{.NetworkSettings.IPAddress}} bookscanlab`
#
#for ((i=3; i>0; i--)) do
#    echo "run delay for $i"
#    sleep 1
#done
#
#address="http://$address:80"
#echo "$address"

#naver-whale --new-tab "$address"

sudo docker attach bookscanlab