import os
from typing import List
from asyncio.log import logger
from dotenv import load_dotenv

import socketio


load_dotenv()

ORIGIN_SOCKET_URL = os.getenv("ORIGIN_SOCKET_URL")


def handle_connect(sid, environ):
    logger.info(f"Socket connected with sid {sid}")


class SocketManager:
    def __init__(self, origins: List[str]):
        self.server = socketio.AsyncServer(
            cors_allowed_origins=origins,
            async_mode="asgi",
            logger=False,
            engineio_logger=False,
        )
        self.app = socketio.ASGIApp(self.server)

    @property
    def on(self):
        return self.server.on

    @property
    def send(self):
        return self.server.send

    @property
    def emit(self):
        return self.server.emit

    @property
    def enter_room(self):
        return self.server.enter_room

    @property
    def leave_room(self):
        return self.server.leave_room

    @property
    def close_room(self):
        return self.server.close_room

    def mount_to(self, path: str, app: socketio.ASGIApp):
        app.mount(path, self.app)


if ORIGIN_SOCKET_URL is None:
    ORIGIN_SOCKET_URL = ""

socket_manager = SocketManager([])
socket_manager.on("connect", handler=handle_connect)


def handle_join(sid, environ):
    socket_manager.enter_room(sid, environ)


socket_manager.on("join", handler=handle_join)


def handle_leave(sid, environ):
    socket_manager.leave_room(sid, environ)


socket_manager.on("leave", handler=handle_leave)


async def handle_close(sid):
    client_rooms = socket_manager.server.rooms(sid)
    if client_rooms[1] is not None:
        await socket_manager.close_room(socket_manager.server.rooms(sid)[1])


socket_manager.on("disconnect", handler=handle_close)
