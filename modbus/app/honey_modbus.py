

from threading import Thread
from modbus.server_slave import ServerSlave
from pymodbus.server.async_io import asyncio


def main():
    s = ServerSlave()
    s.run_server()

if __name__ == "__main__":
    asyncio.run(main())
   