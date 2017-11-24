docker build -t game-server .
docker rm -f game-server
docker run -d -p 50010:50010 --name=game-server game-server
