#!/bin/bash

build='build'
fullbuild='full-build'
buildb='build-b'
buildb='full-build-b'

# 비디오 중단
docker stop bookscanlab
docker rm bookscanlab

# 프론트 빌드
if [ "$1" == 'build' ] || [ "$1" == 'full-build' ] || [ "$1" == 'build-b' ] || [ "$1" == 'full-build-b' ]; then
    cd ./front
    yarn build
    cd ../
fi

# 백엔드 프리 빌드
if [ "$1" == 'full-build' ] || [ "$1" == 'full-build-b' ]; then
    docker build -t bookscanlab-prev ./prev/
fi

# 백엔드 빌드
docker build -t bookscanlab .

# 벡엔드 실행
gnome-terminal -e 'docker run --name bookscanlab -p 80:80 bookscanlab'

# 찌꺼기 이미지 정리
docker rmi $(docker images -f "dangling=true" -q)

# 프론트 실행
address=`docker inspect -f {{.NetworkSettings.IPAddress}} bookscanlab`

address="http://$address:80"
echo "$address"

if [ "$1" == '-b' ] || [ "$1" == 'build-b' ] || [ "$1" == 'full-build-b' ]; then
    for ((i=3; i>0; i--)) do
        echo "run delay for $i"
        sleep 1
    done

    firefox --new-tab "$address"
fi