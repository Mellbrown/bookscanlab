docker stop bookscanlab
docker rm bookscanlab

docker build -t bookscanlab ./app/

docker run -d --name bookscanlab -p 80:80 bookscanlab
