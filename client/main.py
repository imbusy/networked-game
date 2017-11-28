import arcade
import grpc
import logging
import os
import sys

sys.path.append(os.getcwd())

from client.game import GameWindow
from client.network import NetworkThread
import client.settings as settings
import server.interface.game_service_pb2_grpc as gs_grpc
import server.interface.game_service_pb2 as gs

if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    grpc_channel = grpc.insecure_channel(settings.server_address)
    server = gs_grpc.GameStub(grpc_channel)
    response = server.SayHello(gs.HelloRequest(client_version=settings.client_version))
    if not response.valid_client_version:
        logging.error('Client too old. Please update your client.')
        sys.exit()

    logging.info('Running game.')
    window = GameWindow()
    window.setup()
    #network_thread = NetworkThread(window, server)
    #network_thread.start()
    arcade.run()
    #network_thread.finish()
    #network_thread.join(timeout=5)
