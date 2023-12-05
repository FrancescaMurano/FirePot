# import asyncio
# import asyncssh
# import crypt
# import sys
# from typing import Optional
# from elastic.elasticserver import ElasticServer
# from log_requests import Request
# # Importa la logica del codice precedente qui, adattando se necessario

# passwords = {'root': 'root',  # guest account with no password
#              }

# PORT = 2222

# class SSHServer(asyncssh.SSHServer):
#     def __init__(self):
#         super().__init__()

#     def connection_made(self, connection):
#         self.peer_addr = connection.get_extra_info('peername')
#         print(f"Connection from {self.peer_addr[0]}:{self.peer_addr[1]}")

#     def connection_lost(self, exc):
#         print(f"Connection from {self.peer_addr[0]}:{self.peer_addr[1]} closed")

#     def password_auth_supported(self):
#         return True

#     async def auth_password(self, username, password):
#         if username == "root" and password == "root":
#             return True
#         return False

#     def session_requested(self):
#         return SSHSession()

# class SSHSession(asyncssh.SSHServerSession):
#     def __init__(self):
#         super().__init__()
#         self.output = ""
#         self.server = ElasticServer()
#         self.request = None

#     def connection_made(self, chan):
#         self.channel = chan
#         self.request = Request(ip=self.get_extra_info('peername')[0])
#         self.channel.write("Welcome to my async SSH server!\r\n")

#     def data_received(self, data, datatype):
#         command = data.decode('utf-8')

#         if not command:
#             return

#         # Aggiungi qui la logica per gestire gli escape character e comandi specifici

#     def eof_received(self):
#         self.channel.write("Session closed.\r\n")
#         self.channel.close()

#     def connection_lost(self, exc):
#         self.server.channel = None

# async def start_server():
#     await asyncssh.create_server(
#         SSHServer, "", PORT,
#         server_host_keys=['static_host_key']
#     )

# loop = asyncio.get_event_loop()

# try:
#     loop.run_until_complete(start_server())
# except (OSError, asyncssh.Error) as exc:
#     sys.exit('Error starting server: ' + str(exc))

# loop.run_forever()

import asyncio
import asyncssh
from log_requests import Request
from elastic.elasticserver import ElasticServer
from utils.utils_commands import *
from utils.utils_path import Path
import re

PORT = 2222
BANNER = "SSH-2.0-OpenSSH_5.3"
# commands
UP_KEY = "\x1b[A".encode()
DOWN_KEY = "\x1b[B".encode()
RIGHT_KEY = "\x1b[C".encode()
LEFT_KEY = "\x1b[D".encode()
BACK_KEY = "\x7f".encode()

class SSHServer(asyncssh.SSHServer):
    def __init__(self):
        super().__init__()

    def connection_made(self, connection):
        self.channel = None
        self.peer_addr = connection.get_extra_info('peername')
        print(f"Connection from {self.peer_addr[0]}:{self.peer_addr[1]}")

    def connection_lost(self, exc):
        print(f"Connection from {self.peer_addr[0]}:{self.peer_addr[1]} closed")

    def begin_auth(self, username):
        if username == "root":
            return ["password"]
        return []

    def password_auth_supported(self):
        return True

    def validate_password(self, username, password):
        return username == "root" and password == "root"

    def session_requested(self):
        return SSHSession(self)


class SSHSession(asyncssh.SSHServerSession):
    def __init__(self, server):
        super().__init__(server)
        self.output = ""
        self.server = ElasticServer()
        self.request = Request(ip=self.server.peer_addr[0])

    def connection_made(self, chan):
        self.channel = chan
        self.request = Request(ip=self.server.peer_addr[0])
        self.channel.write("Welcome to my async SSH server!\r\n")
        self.channel.write(p.get_cli_display_path().encode('utf-8'))

    def data_received(self, data, datatype):
        command = data.decode('utf-8')

        if not command:
            return

        # escape commands
        if command == UP_KEY or command == DOWN_KEY or command == LEFT_KEY or command == RIGHT_KEY:
            return

        if command == "\r":
            self.channel.write("\r\n".encode('utf-8'))

            multiple_cmds = re.split(r"&&", self.output)
            results = []

            for cmd in multiple_cmds:
                cmd = cmd.lstrip()
                result, error = exec_command(cmd)
                print("error", error)
                # await self.server.insert_ip_request(self.request.get_request_json(cmd))
                results.append(result)

            for res in results:
                res = res.encode("utf-8")
                res = res.replace(b"  ", b"")
                res = res.replace(b"\n", b"\r\n")

                self.channel.write(res)

            self.channel.write(p.get_cli_display_path().encode('utf-8'))

            self.output = ""

        elif command == b"\x7f":  # cancel only user input
            if self.output:
                self.output = self.output[:-1]
                self.channel.write(b'\x08')
                self.channel.write(b' \x08')

        elif command == b'\x03' or command == b"exit":  # command to quit
            self.channel.write("\r\n".encode('utf-8'))
            self.channel.close()

        else:  # concat input
            self.output += command
            self.channel.write(data)

    def eof_received(self):
        self.channel.write("Session closed.\r\n")
        self.channel.close()

    def connection_lost(self, exc):
        self.server.channel = None


async def start_server():
    try:
        await asyncssh.create_server(
            SSHServer, "", PORT,
            server_host_keys=['static_host_key']
        )
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    p = Path()
    try:
        asyncio.run(start_server())
    except Exception as e:
        print(f"An error occurred: {e}")
