"""
Server realisation.
"""
import asyncio
import logging
import random
import shlex


logging.basicConfig(level=logging.INFO)


class Server:
    """_summary_
    """

    rooms = {}
    clients = {}

    async def run(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        """Communicate with clients.

        :param reader: _description_
        :type reader: _type_
        :param writer: _description_
        :type writer: _type_
        """
        ID = '{}:{}'.format(*writer.get_extra_info('peername'))
        personal_queue = asyncio.Queue()
        send = asyncio.create_task(reader.readline())
        receive = asyncio.create_task(personal_queue.get())
        connected = True

        try:
            while connected and not reader.at_eof():
                done, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)
                for task in done:
                    to_other = None
                    response = None
                    if task is send:
                        send = asyncio.create_task(reader.readline())
                        data = task.result().decode().strip()

                        logging.info('received: %s', data)

                        match shlex.split(data):
                            case ['login', login]:
                                if login in self.clients.keys():
                                    response = 'This login is taken'
                                else:
                                    ID = login
                                    self.clients[ID] = personal_queue
                            case ['move', *args]:
                                i0, j0, i1, j1 = args
                                to_other = f'{i0} {j0} {i1} {j1}'
                            case ['new']:
                                # room = 0
                                # while room:=random.randint(0, 10000):
                                #     if room not in self.rooms:
                                #         break

                                room = random.randint(0, 10000)
                                self.rooms[ID] = [room]

                                response = room
                            case ['connect', room]:
                                if room in self.rooms:
                                    self.rooms[ID].append(room)
                            case ['exit']:
                                connected = False
                                response = 'You successfully left'
                            case _:
                                logging.warning('Unknown command: %s', data)

                        if to_other:
                            curr_room = self.rooms[ID]
                            for id_, room in self.rooms.items():
                                if room == curr_room:
                                    q = self.clients[id_]
                                    if q is not personal_queue:
                                        logging.info('Sending "%s" to %s', to_other, id_)
                                        await q.put(to_other)
                                    break

                        if response:
                            q = self.clients[ID]
                            logging.info('Sending "%s" to %s', response, ID)
                            await q.put(to_other)
                            # for other_ID, q in self._clients.items():
                            #     if q is not personal_queue:
                            #         lst = message_to_users if isinstance(message_to_users, list) else [message_to_users]
                            #         for message in lst:
                            #             if isinstance(message, Message):
                            #                 await q.put(self.translate(other_ID, message))
                            #             else:
                            #                 await q.put(message)
                    elif task is receive:
                        receive = asyncio.create_task(personal_queue.get())
                        writer.write(f'{task.result()}\n'.encode())
                        await writer.drain()

            send.cancel()
            receive.cancel()
            writer.close()
            await writer.wait_closed()
        except Exception as e:
            logging.error(e, exc_info=True)

        # if ID in self._clients.keys():
        #     del self._clients[ID]
        #     message_to_users = Message('other_left', [ID])
        #     for other_ID, q in self._clients.items():
        #         await q.put(self.translate(other_ID, message_to_users))


async def start_game() -> None:
    """Initiate server."""
    server = Server()
    playing_server = await asyncio.start_server(server.run, 'localhost', 1337)
    async with playing_server:
        await playing_server.serve_forever()


def main() -> None:
    """entering point
    """
    logging.info('Starting server')
    asyncio.run(start_game())
