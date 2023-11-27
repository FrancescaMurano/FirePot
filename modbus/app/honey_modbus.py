from twisted.internet.task import LoopingCall
from threading import Thread
from modbus.server_slave import ServerSlave

s = ServerSlave()

# Start
t2 = Thread(target=s.run_server).start()
loop = LoopingCall(f=s.read_file)
loop.start(5, now=False) # initially delay by time
