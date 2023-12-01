import asyncio
import re
import socket
from subprocess import *
from elastic.elasticserver import ElasticServer
from utils.utils_path import *
from utils.utils_commands import exec_command
from log_requests import Request


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
    ip = writer.get_extra_info('peername')[0]
    elastic = ElasticServer()
    request = Request(ip)

    output = ""

    START = p.get_cli_display_path().encode('utf-8',errors='ignore')
    writer.write(START)

    try:
        while True:
            command: bytes = await reader.read(100000)

            if not command:
                print("no command")
                break

            # escape commands
            if command == UP_KEY or command == DOWN_KEY or command == LEFT_KEY or command == RIGHT_KEY:
                continue

            if command.endswith(b"\r\n"):
                output += command.decode('utf-8',errors='ignore')
                multiple_cmds = re.split(r"&&", output)
                results = []

                multiple_cmds = [item for item in multiple_cmds if item != '']
                for cmd in multiple_cmds:
                    cmd = cmd.strip()
                    try:
                        result, error = exec_command(cmd)
                       # elastic.insert_ip_request(request.get_request_json(cmd))
                        results.append(result)
                    except CalledProcessError as e:
                        writer.write("Error: the sintax of the command is incorrect\r\n".encode("utf-8").strip())
                        writer.write(p.get_cli_display_path().encode('utf-8',errors='ignore'))
                        print(f"Error: {str(e)}")
                        output = ""

                for res in results:
                    res = res.encode("utf-8").strip()
                    res = res.replace(b"  ", b"")
                    res = res.replace(b"\n", b"\r\n")
                    writer.write(res)

                writer.write(p.get_cli_display_path().encode('utf-8',errors='ignore'))
                output = ""

            elif command == b"\x08":  # cancel only user input
                if output:
                    output = output[:-1]
                    writer.write(b' \x08')
                    writer.write(b' \x08')

            elif command == b'\x03':  # command to quit
                writer.write("\r\n".encode('utf-8',errors='ignore'))
                break  # exit the loop when client sends Ctrl+C

            # else:  # concat input
                

    except asyncio.CancelledError:
        pass  # Handle cancellation errors gracefully

    except (ConnectionResetError, BrokenPipeError):
        pass  # Handle specific socket errors

    # except Exception as e:
    #     writer.write(f"Error: {str(e)}\r\n".encode("utf-8").strip())
    #     writer.write(p.get_cli_display_path().encode('utf-8',errors='ignore'))
    #     print(f"Error: {str(e)}")
    #     output = ""

    finally:
        #elastic.insert_ip_data(request.get_ip_info())
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