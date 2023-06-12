"""
Server realisation.
"""
import asyncio
import os
import random
import shlex
import uuid


class Server:
    """_summary_
    """

    clients = {}
    players = {}

    async def run(self, reader, writer):
        """Communicate with clients.

        :param reader: _description_
        :type reader: _type_
        :param writer: _description_
        :type writer: _type_
        """
        ...


async def start_game() -> None:
    """Initiate server."""
    server = Server()
    playing_server = await asyncio.gather(
        asyncio.start_server(server.run, '0.0.0.0', 8080),
        server.monster_motion()
        )
    async with playing_server:
        await playing_server.serve_forever()


def main() -> None:
    asyncio.run(start_game())
