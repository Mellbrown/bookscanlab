#!/bin/bash
export DOCKER_HOST=tcp://localhost:2375

# 비디오 중단
docker stop bookscanlab
docker rm bookscanlab

# 프론트 빌드
if [ "$1" == '-f' ]; then
    cd ./front
    yarn build
    cd ../
    docker build -t bookscanlab-prev ./prev/
fi

# 백엔드 빌드
docker build -t bookscanlab ./app/

# 벡엔드 실행
docker run -d --name bookscanlab -p 80:80 bookscanlab

# 찌꺼기 이미지 정리
docker rmi $(docker images -f "dangling=true" -q)
