from config import *
from core.server import GameServer

server = GameServer(HOST, PORT)
server.start()
