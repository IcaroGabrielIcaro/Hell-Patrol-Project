from server.config import *
from server.core.server import GameServer

server = GameServer(HOST, PORT)
server.start()
