from twisted.internet.task import LoopingCall
from threading import Thread
from modbus.server_slave import ServerSlave
from twisted.internet import reactor
from twisted.internet.threads import deferToThread

def update_info_log():
    s = ServerSlave()
    deferToThread(s.read_file)

def main():
    if not reactor.running:
        loop = LoopingCall(f=update_info_log)
        loop.start(5, now=False) # initially delay by time
    
        reactor.run()
   

if __name__ == "__main__":
    s = ServerSlave()
    s.run_server()
    main()