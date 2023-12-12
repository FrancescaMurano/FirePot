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


paramiko.util.log_to_file("paramiko.log", level=paramiko.util.DEBUG)

PORT = 2222
BANNER = "SSH-2.0-OpenSSH_5.3"

# commands
UP_KEY = "\x1b[A".encode()
DOWN_KEY = "\x1b[B".encode()
RIGHT_KEY = "\x1b[C".encode()
LEFT_KEY = "\x1b[D".encode()
BACK_KEY = "\x7f".encode()

class SSHServer(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()
        self.banner_timeout = 60

    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        if username == "root" and password == "root":
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
    # Allow PTY allocation
        return True

    def check_channel_shell_request(self, channel):
    # Allow the shell request
        return True
 
    def get_banner(self):
        return ("SSH-2.0-OpenSSH_5.3\n",'en-US')

# Create a socket for the SSH server


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
        p.reset_path()
    
        channel = transport.accept(20)

        if channel is None:
            print("No session created.")
            transport.close()
            continue
        else:
            channel.send(START)

        output = ""
        server = ElasticServer()
        request = Request(ip=addr[0])
        channel.settimeout(10)

        while True:

            START = p.get_cli_display_path().encode('utf-8')
            
            try:
                command = channel.recv(2048)

                if not command:
                    print("no command")
                    break

                # excape commands
                if command == UP_KEY or command == DOWN_KEY or command == LEFT_KEY or command == RIGHT_KEY:
                    continue

                if command == b"\r":
                    channel.send("\r\n".encode('utf-8'))  

                    multiple_cmds = re.split(r"&&", output)
                    results = []

                    for cmd in (multiple_cmds):
                        cmd = cmd.lstrip()
                        result,error = exec_command(cmd)
                        if error:
                            print("error",error)
                        await server.insert_ip_request(request.get_request_json(cmd))
                        results.append(result)
                    
                    for res in results:
                        res = res.encode("utf-8")
                        res = res.replace(b"  ",b"")
                        res = res.replace(b"\n",b"\r\n")

                        channel.send(res)

                    channel.send(p.get_cli_display_path().encode('utf-8'))

                    output = ""

                elif command == b"\x7f": # cancel only user input 
                    if output: 
                        output = output[:-1]
                        channel.send(b'\x08')
                        channel.send(b' \x08')


                elif command == b'\x03' or command == b"exit": # command to quit
                        channel.send("\r\n".encode('utf-8'))
                        transport.close()
                        
                else: # concat imput
                    output+= command.decode('utf-8')
                    channel.send(command)

            except socket.timeout:
                print("Timeout")
                channel.close()
                
            except Exception as e:
                import traceback
                traceback.print_exc()
                channel.send("An error occurred. Check the server logs for details.\r\n".encode("utf-8"))
                channel.send(p.get_cli_display_path().encode('utf-8'))
                output = ""
        
        await server.insert_ip_data(request.get_ip_info())
        
        channel.close()
        transport.close()


if __name__ == "__main__":
    asyncio.run(main())