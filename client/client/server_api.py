import readline
import socket


BUFFER_SIZE = 1024


class ServerAPI:
    """Class for communication with server
    """
    def __init__(self, host: str = 'localhost', port: int = 1337) -> None:
        self.buffer_size = BUFFER_SIZE
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))

    def stop(self) -> None:
        """stop communication with server
        """
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()

    def send(self, msg: str) -> None:
        """send message

        :param msg: message to send
        :type msg: str
        """
        self.socket.send(f'{msg}\n'.encode())

    def receive(self):
        """receive message
        """
        # TODO(marilius): распарить + порядок сообщений?
        while True:
            responses = self.socket.recv(self.buffer_size).decode()
            for response in responses.split('\n'):
                if response:
                    print(f'\r{response}\n{readline.get_line_buffer()}', end='', flush=True)
