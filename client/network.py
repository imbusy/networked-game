import logging
import threading
import time

from client.game import GameWindow
import client.settings as settings
import server.interface.game_service_pb2_grpc as gs_grpc
import server.interface.game_service_pb2 as gs


class NetworkThread(threading.Thread):
    def __init__(self, game: GameWindow, server: gs_grpc.GameStub):
        super().__init__()
        self.finished = False
        self.server = server
        self.game = game

    def finish(self):
        logging.info('Finishing network thread.')
        self.finished = True

    def run(self):
        while not self.finished:
            #response = self.server.GetState(gs.GetStateRequest())
            #self.game.update_state(response)
            time.sleep(1.0)
        logging.info('Network thread finished.')