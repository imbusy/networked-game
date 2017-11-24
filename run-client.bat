python -m grpc_tools.protoc -I./protos --python_out=./server/interface --grpc_python_out=./server/interface ./protos/game_service.proto
python client/main.py