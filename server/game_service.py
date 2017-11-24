import server.interface.game_server_pb2_grpc as gs_grpc
import server.interface.game_server_pb2 as gs
import server.settings as settings

class GameService(gs_grpc.GameServicer):
	def SayHello(self, request, context):
   		return gs.HelloReply(
   			valid_client_version=(request.client_version>=settings.min_client_version),
   			server_version=settings.server_version)
