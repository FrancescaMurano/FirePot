import asyncio
import re
from subprocess import *
from utils.utils_path import *
from utils.utils_commands import exec_command

PORT = 2323
BANNER = "Telnet"
p = Path()

# commands
UP_KEY = "\x1b[A".encode()
DOWN_KEY = "\x1b[B".encode()
RIGHT_KEY = "\x1b[C".encode()
LEFT_KEY = "\x1b[D".encode()
BACK_KEY = "\x7f".encode()

 

async def handle_client(reader, writer):
    print(f"Connected to {writer.get_extra_info('peername')}")
    output = ""
    START = p.get_cli_display_path().encode('utf-8')
    writer.write(START) 
    while True:
        try:
            command : bytes = await reader.read(100000)
            if not command:
                print("no command")
                break

            # excape commands
            if command == UP_KEY or command == DOWN_KEY or command == LEFT_KEY or command == RIGHT_KEY:
                continue

            if command == b"\r\n":
                multiple_cmds = re.split(r"[;&&]", output)
                results = []

                for cmd in (multiple_cmds):
                    cmd = cmd.lstrip()
                    result,error = exec_command(cmd)
                    #server.insert_ip_request(request.get_request_json(cmd))
                    results.append(result)
                
                for res in results:
                    writer.write(res.encode("utf-8"))
                
                writer.write(p.get_cli_display_path().encode('utf-8'))

                output = ""

            elif command == b"\x08": # cancel only user input 
                if output: 
                    output = output[:-1]
                    print("out",output)
                    writer.write(b' \x08')
                    writer.write(b' \x08')

            elif command == b'\x03': # command to quit
                    writer.write("\r\n".encode('utf-8'))
                    writer.close()
                     
            else: # concat imput
                output+= command.decode('utf-8')

        except Exception as e:
            writer.write("Error: the sintax of the command is incorrect\r\n".encode("utf-8"))
            writer.write(p.get_cli_display_path().encode('utf-8'))
            output = ""
            
    print("Closing connection")
    writer.close()
 
 
async def start_server():
    server = await asyncio.start_server(handle_client, "0.0.0.0", PORT)
    print("Server started")
    await server.serve_forever()
 
asyncio.run(start_server())
