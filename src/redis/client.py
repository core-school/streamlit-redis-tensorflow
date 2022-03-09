from asyncio_redis import Connection
from config import REDIS_HOST, REDIS_PORT

global connections
connections = dict()

DEFAULT_CONNECTION = "default"


async def connect(connection_id=DEFAULT_CONNECTION):
    global connections
    #print(f"Connecting Redis on {REDIS_HOST}:{REDIS_PORT} ...")
    connections[connection_id] = await Connection.create(host=REDIS_HOST, port=int(REDIS_PORT))
    print(f"✅ Redis is connected {connection_id}")
    return connections[connection_id]


async def disconnect(connection_id=DEFAULT_CONNECTION):
    global connections
    c = connections.get(connection_id)
    # When finished, close the connection.
    c.close()
    print(f"❌ Redis disconnected {connection_id}")


def get_connection(connection_id=DEFAULT_CONNECTION):
    global connections
    c = connections.get(connection_id)
    if not c:
        raise ValueError(f"You should call connect('{connection_id}') first")
    return c
