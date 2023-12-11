import asyncio
from typing import Mapping, Tuple
import asyncssh
import re
from asyncssh.connection import SSHServerConnection
from utils.utils_path import Path
from asyncssh.misc import MaybeAwait
from utils.utils_commands import exec_command
from log_requests import Request
from elastic.elasticserver import ElasticServer

PORT = 2222
BANNER = "SSH-2.0-OpenSSH_5.3"

UP_KEY = "\x1b[A".encode()
DOWN_KEY = "\x1b[B".encode()
RIGHT_KEY = "\x1b[C".encode()
LEFT_KEY = "\x1b[D".encode()
BACK_KEY = "\x7f".encode()


class SSHServer(asyncssh.SSHServer):
    def __init__(self):
        super().__init__()

    def session_requested(self):
        return SSHSession()

    def password_auth_supported(self):
        return True

    def validate_password(self, username, password):
        # Valida la password (in questo esempio, accetta qualsiasi password per l'utente "root")
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
            # Get the client's address (IP and port)
            peer_addr = chan.get_extra_info('peername')
            if peer_addr:
                self.client_ip = peer_addr[0]
            else:
                self.client_ip = "Unknown"

            self.request = Request(self.client_ip)

    def pty_requested(self, term_type: str, term_size: Tuple[int, int, int, int], term_modes: Mapping[int, int]) -> bool:
        return True

    def shell_requested(self) -> bool:
        return True


    def get_banner(self):
        return ("SSH-2.0-OpenSSH_5.3\n",'en-US')

    def data_received(self, data:str, datatype):
        try:
            command = data.encode("utf-8")
            if command.endswith(b"\n"):
                self.chan.write("\r\n")
                multiple_cmds = re.split(r"&&", data)
                results = []

                for cmd in multiple_cmds:
                    cmd = cmd.lstrip()
                    print("cmd ",cmd)
                    result, error = exec_command(cmd)
                    print("result ",result)
                    if error:
                        print("error", error)
                    #self.server.insert_ip_request(self.request.get_request_json(cmd))
                    results.append(result)

                for res in results:
                    res = res.encode("utf-8")
                    res = res.replace(b"  ", b"")
                    res = res.replace(b"\n", b"\r\n")
                    self.chan.write(res.decode("utf-8"))

                self.chan.write(self.path.get_cli_display_path())
                # self.output = ""

            elif command == b"\x7f":  # cancel only user input
                if self.output:
                    self.output = self.output[:-1]
                    self.chan.write(b'\x08')
                    self.chan.write(b' \x08')

            elif command == b'\x03' or command == b"exit":  # command to quit
                self.chan.write("\r\n".encode('utf-8'))
                self.chan.exit(0)
            
        except Exception as e:
            print(str(e))

        # else:  # concat input
        #     self.output += command
        #     self.chan.write(data)


async def start_server():
    await asyncssh.create_server(
        lambda *args, **kwargs: SSHServer(),
        '0.0.0.0', PORT,
        server_host_keys=['static_host_key'],
        # authorized_client_keys='ssh_user_ca'
    )

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_server())
    loop.run_forever()
