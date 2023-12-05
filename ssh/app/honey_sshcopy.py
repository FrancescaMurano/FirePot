import threading
import paramiko
import re
import socket
import os
from subprocess import *
from utils.utils_commands import *
from log_requests import Request
from elastic.elasticserver import ElasticServer
import asyncio
from datetime import datetime, timedelta
from collections import defaultdict

paramiko.util.log_to_file("paramiko.log", level=paramiko.util.DEBUG)

PORT = 2222
BANNER = "SSH-2.0-OpenSSH_5.3"

# commands
UP_KEY = "\x1b[A".encode()
DOWN_KEY = "\x1b[B".encode()
RIGHT_KEY = "\x1b[C".encode()
LEFT_KEY = "\x1b[D".encode()
BACK_KEY = "\x7f".encode()

MAX_CONCURRENT_CONNECTIONS = 100
MAX_BANDWIDTH = 1024  # Limite di banda in kilobits per secondo
IDLE_TIMEOUT = 300  # Timeout di 5 minuti per inattività
MAX_REQUESTS_PER_IP = 10  # Numero massimo di richieste da un singolo IP in un intervallo di tempo

# Dizionario per tenere traccia del numero di richieste da parte di ogni indirizzo IP
requests_per_ip = defaultdict(int)
# Dizionario per tenere traccia dell'ultimo momento in cui è stata effettuata una richiesta da parte di ogni indirizzo IP
last_request_time = defaultdict(datetime)
# Semaforo per limitare il numero massimo di connessioni simultanee
connection_semaphore = threading.BoundedSemaphore(MAX_CONCURRENT_CONNECTIONS)


class SSHServer(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()
        self.banner_timeout = 60

    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        # Allow PTY allocation
        return True

    def check_channel_shell_request(self, channel):
        channel.settimeout(IDLE_TIMEOUT)
        channel.set_combine_stderr(True)
        return True

    def check_auth_password(self, username, password):
        if username == "root" and password == "root":
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        # Allow PTY allocation
        return True

    def check_channel_shell_request(self, channel):
        channel.settimeout(IDLE_TIMEOUT)
        return True

    def get_banner(self):
        return ("SSH-2.0-OpenSSH_5.3\n", 'en-US')


async def main():
    p = Path()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', PORT))
    START = p.get_cli_display_path().encode('utf-8')

    server_socket.listen(5)

    print("Waiting for SSH connections...")

    # Generate the host key file (if it doesn't exist)
    host_key_file = "static_host_key"
    host_key = paramiko.RSAKey.generate(2048)

    if not os.path.exists(host_key_file):
        print("not exists")
        host_key.write_private_key_file(host_key_file)

    while True:
        client_socket, addr = server_socket.accept()

        # Acquire the semaphore to limit the number of concurrent connections
        connection_semaphore.acquire()

        # Check if the number of requests from the IP exceeds the limit in the given time frame
        if requests_per_ip[addr[0]] >= MAX_REQUESTS_PER_IP and \
                datetime.now() - last_request_time[addr[0]] < timedelta(seconds=IDLE_TIMEOUT):
            print(f"Connection from {addr[0]} refused due to excessive requests.")
            connection_semaphore.release()
            continue

        transport = paramiko.Transport(client_socket)
        transport.local_version = BANNER

        # Load the static host key
        transport.load_server_moduli()
        transport.add_server_key(host_key)

        server = SSHServer()

        try:
            transport.start_server(server=server)
        except paramiko.SSHException as ssh:
            print(ssh)
        except ConnectionResetError as connectionerror:
            print(connectionerror)
        except EOFError as oeferror:
            print(oeferror)

        print(f"Connection from {addr[0]}:{addr[1]}")

        channel = transport.accept(20)

        if channel is None:
            print("No session created.")
            transport.close()
            connection_semaphore.release()
            continue
        else:
            channel.send(START)

        output = ""
        server = ElasticServer()
        request = Request(ip=addr[0])

        while True:
            START = p.get_cli_display_path().encode('utf-8')

            try:
                command = channel.recv(1024)
                print("command", command)

                if not command:
                    print("no command")
                    break

                # Escape commands
                if command == UP_KEY or command == DOWN_KEY or command == LEFT_KEY or command == RIGHT_KEY:
                    continue

                # Update the request count and time for the IP
                requests_per_ip[addr[0]] += 1
                last_request_time[addr[0]] = datetime.now()

                if command == b"\r":
                    channel.send("\r\n".encode('utf-8'))

                    multiple_cmds = re.split(r"&&", output)
                    results = []

                    for cmd in multiple_cmds:
                        cmd = cmd.lstrip()
                        result, error = exec_command(cmd)
                        print("error", error)
                        # await server.insert_ip_request(request.get_request_json(cmd))
                        results.append(result)

                    for res in results:
                        res = res.encode("utf-8")
                        res = res.replace(b"  ", b"")
                        res = res.replace(b"\n", b"\r\n")

                        channel.send(res)

                    channel.send(p.get_cli_display_path().encode('utf-8'))

                    output = ""

                elif command == b"\x7f":  # Cancel only user input
                    if output:
                        output = output[:-1]
                        channel.send(b'\x08')
                        channel.send(b' \x08')

                elif command == b'\x03' or command == b"exit":  # Command to quit
                    channel.send("\r\n".encode('utf-8'))
                    transport.close()

                else:  # Concat input
                    output += command.decode('utf-8')
                    channel.send(command)

            except socket.timeout:
                channel.close()

            except Exception as e:
                import traceback
                traceback.print_exc()
                channel.send("An error occurred. Check the server logs for details.\r\n".encode("utf-8"))
                channel.send(p.get_cli_display_path().encode('utf-8'))
                output = ""

        # await server.insert_ip_data(request.get_ip_info())

        channel.close()
        transport.close()
        connection_semaphore.release()


if __name__ == "__main__":
    asyncio.run(main())
