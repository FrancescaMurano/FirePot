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
FULL_PATH = os.path.join(ABSOLUTE_PATH, RELATIVE_PATH)


# Create a class to handle SSH connections
class SSHServer(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        if username == "root" and password == "root":
            print("login success")
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
    # Allow PTY allocation
        return True

    def check_channel_shell_request(self, channel):
    # Allow the shell request
        return True
    
    def welcome_message(self):
        return "=========-- Welcome to SSH Service --=========================\n".encode('utf-8')
   

# Create a socket for the SSH server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', PORT))


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
    # Load the static host key
    transport.load_server_moduli()
    transport.add_server_key(host_key)

    server = SSHServer()
    
    transport.start_server(server=server)

    print(f"Connection from {addr[0]}:{addr[1]}")

 
    channel = transport.accept(20)

    if channel is None:
        print("No session created.")
        transport.close()
        continue
    else:
        channel.send(server.welcome_message())
        channel.send("\n".encode('utf-8'))


    output = ""
    while True:
        try:
            command = channel.recv(2048)
            if not command:
                print("no command")
                break
            if command == b"\r":
                print("output ",output)
                cmds = re.split(';&&,| ', output)

                print("cmds ",cmds)
                if cmds[0] == "dir":
                    command_cmd = f" cd {FULL_PATH} && {output}"
                    result = subprocess.check_output(command_cmd, shell=True)
                    channel.send("\n"+result.decode("utf-8"))
                
                elif cmds[0] == "type":
                    command_cmd = f" cd {FULL_PATH} && {output}"
                    result = subprocess.check_output(command_cmd, shell=True)
                    channel.send("\n"+result.decode("utf-8"))

                elif cmds[0] == "echo":
                    command_cmd = f" cd {FULL_PATH} && {output}"
                    result = subprocess.check_output(command_cmd, shell=True)
                    channel.send("\n"+result.decode("utf-8"))

                elif cmds[0] == "q":
                    channel.send("\n".encode('utf-8'))
                    transport.close()
                    break
             
                # result = f"Command received: {output}\r"
                # channel.send(result.encode('utf-8'))
                channel.send("\r".encode('utf-8'))

                output = ""
            elif command == b"\x7f":
                print("cancel")
                output = output[:-1]
                print("output ",output)
                channel.send(output)

            else:
                output+= command.decode('utf-8')
                channel.send(command.decode('utf-8'))

        except Exception as e:
            print(f"Error: {str(e)}")
            break

    channel.close()
    transport.close()
