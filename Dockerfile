FROM python:3.6

WORKDIR /usr/src/app
RUN pip install --no-cache-dir grpcio grpcio-tools

COPY . .
RUN python -m grpc_tools.protoc \
  -I./protos \
  --python_out=./server/interface \
  --grpc_python_out=./server/interface \
  ./protos/game_service.proto

CMD ["python", "./server/main.py"]
