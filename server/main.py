from concurrent import futures
import grpc
import logging
import os
import sys
import time

sys.path.append(os.getcwd())

import server.interface.game_service_pb2_grpc as gs_grpc
import server.interface.game_service_pb2 as gs
import server.settings as settings
import server.game_service as game_service

def serve():
	server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
	gs_grpc.add_GameServicer_to_server(game_service.GameService(), server)
	server.add_insecure_port('[::]:{port}'.format(port=settings.server_port))

	logging.info('Starting service at port {port}.'.format(port=settings.server_port))
	server.start()
	try:
		while True:
			time.sleep(60 * 60 * 24)
	except KeyboardInterrupt:
		server.stop(0)

if __name__ == '__main__':
	logging.basicConfig(stream=sys.stdout, level=logging.INFO)
	serve()
