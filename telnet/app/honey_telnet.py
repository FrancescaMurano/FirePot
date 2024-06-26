# Copyright (c) 2024 Francesca Murano
# 
# This file is part of the thesis project at the University of Calabria.
# 
# This project is licensed under the MIT License - see the LICENSE file for details.

import asyncio
from subprocess import *
from elastic.elasticserver import ElasticServer
from utils.utils_path import *
from utils.utils_commands import exec_command
from log_requests import Request
import os
PORT = os.getenv("TELNET_REAL_PORT",2323)

BANNER = "Telnet"


# skip commands
UP_KEY = "\x1b[A".encode()
DOWN_KEY = "\x1b[B".encode()
RIGHT_KEY = "\x1b[C".encode()
LEFT_KEY = "\x1b[D".encode()
BACK_KEY = "\x7f".encode()

async def handle_client(reader, writer):
    ip = writer.get_extra_info('peername')[0]
    elastic = ElasticServer()
    request = Request(ip)
    path = Path()
    output = ""

    START = path.get_cli_display_path().encode('utf-8',errors='ignore')
    writer.write(START)

    try:
        while True:
            command: bytes = await reader.read(100000)
            output += command.decode('utf-8',errors='ignore')

            if not command:
                print("no command")
                break

            # escape commands
            if command == UP_KEY or command == DOWN_KEY or command == LEFT_KEY or command == RIGHT_KEY:
                continue
            
            if output.endswith("\r\n"):
                if output.startswith("exit"):
                    break

                multiple_cmds = output.split("&&")
                results = []
                multiple_cmds = [item for item in multiple_cmds if item != '']

                for cmd in multiple_cmds:
                    cmd = cmd.strip()
                    try:
                        result, error = exec_command(cmd,path)
                        elastic.insert_ip_request(request.get_request_json(cmd))
                        results.append(result)
                        if result == "":
                            results.append(error)
                    except (CalledProcessError,ValueError) as e:
                        print(f"Error: {str(e)}")
                        output = ""

                for res in results:
                    res = res.encode("utf-8")
                    res = res.replace(b"  ", b"")
                    res = res.replace(b"\n", b"\r\n")
                    writer.write(res)

                writer.write(path.get_cli_display_path().encode('utf-8',errors='ignore'))
                output = ""

            elif command == b'\x08':  # cancel only user input
                if len(output) > 0:
                    output = output[:-2]
                    writer.write(b' \x08')
                    writer.write(b' \x08')
            elif command == b'\x03' or command == b"\xff\xf4\xff\xfd\x06" or command==b'exit':  # command to quit
                writer.write("\r\n".encode('utf-8',errors='ignore'))
                break  # exit the loop when client sends Ctrl+C


    except asyncio.CancelledError:
        pass  # Handle cancellation errors gracefully

    except (ConnectionResetError, BrokenPipeError):
        pass  # Handle specific socket errors
    except Exception as e:
        print(str(e))

    finally:
        elastic.insert_ip_data(request.get_ip_info())
        print("Closing connection")
        writer.close()

async def start_server():
    server = await asyncio.start_server(handle_client, "0.0.0.0", PORT)
    print("Server started")
    await server.serve_forever()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(start_server())
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()