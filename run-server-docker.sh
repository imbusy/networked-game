docker build -t game-server .
docker rm -f game-server
docker run -d -p 50000:50000 --name=game-server game-server
