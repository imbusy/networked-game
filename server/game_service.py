import server.interface.game_service_pb2_grpc as gs_grpc
import server.interface.game_service_pb2 as gs
import server.settings as settings


class GameService(gs_grpc.GameServicer):
    def __init__(self):
        self.last_location = (0, 0)

    def SayHello(self, request, context):
        return gs.HelloReply(
            valid_client_version=(request.client_version>=settings.min_client_version),
            server_version=settings.server_version)

    def GetState(self, request: gs.GetStateRequest, context):
        return gs.StateResponse(
            location_x=self.last_location[0],
            location_y=self.last_location[1],
        )

    def UpdateLocation(self, request: gs.UpdateLocationRequest, context):
        self.last_location = (request.x, request.y)
        return gs.StateResponse()
