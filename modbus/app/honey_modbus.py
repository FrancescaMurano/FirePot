

from modbus.server_slave import ServerSlave
from pymodbus.server.async_io import asyncio

s = ServerSlave()
s.run_server()

   