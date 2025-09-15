import consul
import grpc

from bot_gateway.core.config import settings
from bot_gateway.grpc_clients.protos import auth_pb2, auth_pb2_grpc


class AuthServiceClient:
    def __init__(self):
        self.consul_client = consul.Consul(host=settings.CONSUL_HOST, port=settings.CONSUL_PORT)
        self.auth_service_address = self._get_auth_service_address()

    def _get_auth_service_address(self):
        _, services = self.consul_client.health.service("auth_service")
        if not services:
            raise Exception("Auth service not found in Consul")
        service = services[0]["Service"]
        return f"{service['Address']}:{service['Port']}"

    async def get_user(self, user_id: int):
        async with grpc.aio.insecure_channel(self.auth_service_address) as channel:
            stub = auth_pb2_grpc.AuthServiceStub(channel)
            response = await stub.GetUser(auth_pb2.GetUserRequest(user_id=user_id))
            return response.user