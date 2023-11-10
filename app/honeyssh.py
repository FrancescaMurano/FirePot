import subprocess
import threading
import paramiko
import re
import socket
import os
from subprocess import *

paramiko.util.log_to_file("paramiko.log", level=paramiko.util.DEBUG)

PORT = 2222
ABSOLUTE_PATH = os.path.dirname(__file__)
RELATIVE_PATH = "home"
START_FULL_PATH = os.path.join(ABSOLUTE_PATH, RELATIVE_PATH)
START = '\r\ndebian@root: '.encode('utf-8')
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
        self.banner_timeout = 200 # It was 15


    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        if username == "root" and password == "root":
            # print("login success")
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
    # Allow PTY allocation
        return True

    def check_channel_shell_request(self, channel):
    # Allow the shell request
        return True

# Create a socket for the SSH server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', PORT))


server_socket.listen(5)

print("Waiting for SSH connections...")

current_path = START_FULL_PATH
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

    except paramiko.SSHException:
        raise Exception("SSH connection failed.")
    except ConnectionResetError as connectionerror:
        print(connectionerror)

    print(f"Connection from {addr[0]}:{addr[1]}")

 
    channel = transport.accept(20)

    if channel is None:
        print("No session created.")
        transport.close()
        continue
    else:
        # channel.send(server.welcome_message())
        channel.send(START)


    output = ""
    while True:
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

                print("output ",output)

                multiple_cmds = re.split(r"[;&&]", output)

                for cmd in multiple_cmds:
                    cmd = cmd.lstrip()
                    prefix = ("dir","ls","type","echo","cat","clear")
                    if cmd.startswith(prefix):
                        result = subprocess.run(output, shell=True,cwd=current_path, stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
                        channel.send(result.stdout)
                        channel.send(START)

                    elif cmd.startswith("whoami"):
                        channel.send("root\debian")
                        channel.send(START)
                    
                    elif cmd.startswith("pwd"):
                        channel.send("home")
                        channel.send(START)
                    
                    elif cmd.startswith("cd"):
                        if ".." in cmd or "-" in cmd:
                            result = subprocess.run("cd .", shell=True,cwd=START_FULL_PATH, stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
                            current_path = START_FULL_PATH
                        else:
                            result = subprocess.run(output, shell=True,cwd=START_FULL_PATH, stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
                            current_path = os.path.join(START_FULL_PATH,cmd.split(" ")[1])

                            channel.send(result.stdout)

                        channel.send(START)

                    else:
                        channel.send("Error: the sintax of the command is incorrect")
                        channel.send(START)


                output = ""

            elif command == b"\x7f":
                if output: # cancel only user input 
                    output = output[:-1]
                    channel.send(b'\x08')
                    channel.send(b' \x08')


            elif command == b'\x03':
                    channel.send("\r\n".encode('utf-8'))
                    transport.close()
                    
            else:
                output+= command.decode('utf-8')
                channel.send(command)

        except Exception as e:
            print(f"Error: {str(e)}")

            channel.send("Error: the sintax of the command is incorrect\r\n".encode("utf-8"))
            channel.send(str(e).encode("utf-8"))

            channel.send(START)
            output = ""


    channel.close()
    transport.close()
