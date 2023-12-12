
docker-compose up

cd ssh && docker build -t ssh . && docker run --name=ssh -d -p 22:2222 ssh