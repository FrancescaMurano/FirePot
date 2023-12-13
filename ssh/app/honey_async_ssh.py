import asyncio
from typing import Mapping, Optional, Tuple
import asyncssh
import re
from utils.utils_path import Path
from utils.utils_commands import exec_command
from log_requests import Request
from elastic.elasticserver import ElasticServer


import os
valore1 = os.getenv("VALORE1",2222)
PORT = valore1


BANNER = "SSH-2.0-OpenSSH_5.3"

import tracemalloc

tracemalloc.start(15)
UP_KEY = "\x1b[A".encode()
DOWN_KEY = "\x1b[B".encode()
RIGHT_KEY = "\x1b[C".encode()
LEFT_KEY = "\x1b[D".encode()
BACK_KEY = "\x7f".encode()


class SSHServer(asyncssh.SSHServer):
    def __init__(self):
        super().__init__()
    
    def connection_made(self, conn: asyncssh.SSHServerConnection):
        conn.send_auth_banner('SSH-2.0-OpenSSH_5.3\n')
        super().connection_made(conn)

    def session_requested(self):
        return SSHSession()

    def password_auth_supported(self):
        return True

    def validate_password(self, username, password):
        return username == 'root' and password == 'root'

   
class SSHSession(asyncssh.SSHServerSession):
    def __init__(self):
        super().__init__()
        self.output = ""
        self.server = ElasticServer()
        self.request = None
        self.path = Path()

    def connection_made(self, chan):
            self.chan = chan
            peer_addr = chan.get_extra_info('peername')
            self.chan.write(self.path.get_cli_display_path())
            if peer_addr:
                self.client_ip = peer_addr[0]
            else:
                self.client_ip = "Unknown"

            self.request = Request(self.client_ip)

    def pty_requested(self, term_type: str, term_size: Tuple[int, int, int, int], term_modes: Mapping[int, int]) -> bool:
        return True

    def shell_requested(self) -> bool:
        return True

    def data_received(self, data:str, datatype):
        try:
            command = data.encode("utf-8")

            if command == b'\x03\n' or command == b'exit\n':  # command to quit
                self.chan.exit(0)
                
            elif command.endswith(b"\n"):
                self.chan.write("\r\n")
                multiple_cmds = re.split(r"&&", data)
                results = []

                for cmd in multiple_cmds:
                    cmd = cmd.lstrip()
                    result, error = exec_command(cmd,self.path)
                    if error:
                        print("error", error)
                    self.server.insert_ip_request(self.request.get_request_json(cmd))
                    results.append(result)

                for res in results:
                    res = res.encode("utf-8")
                    self.chan.write(res.decode("utf-8"))

                self.chan.write(self.path.get_cli_display_path())

            elif command == b"\x7f":  # cancel only user input
                if self.output:
                    self.output = self.output[:-1]
                    self.chan.write(b'\x08')
                    self.chan.write(b' \x08')
        except Exception as e:
            print(str(e))

    def connection_lost(self, exc: Optional[Exception]) -> None:
        self.server.insert_ip_data(self.request.get_ip_info())  
        return super().connection_lost(exc)


async def start_server():
    await asyncssh.create_server(
        lambda *args, **kwargs: SSHServer(),
        '0.0.0.0', PORT,
        server_host_keys=['static_host_key'])

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_server())
    loop.run_forever()
