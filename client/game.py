import logging

import server.interface.game_service_pb2_grpc as gs_grpc

def run(server: gs_grpc.GameStub):
	logging.info('Running game.')
