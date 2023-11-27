from twisted.internet.task import LoopingCall
from threading import Thread
from modbus.server_slave import ServerSlave
from twisted.internet import reactor
from twisted.internet.threads import deferToThread
import time

def run_server():
    s = ServerSlave()
    s.run_server()

def update_info_log():
    s = ServerSlave()
    while True:
        s.read_file()
        time.sleep(5)

def main():
    server_thread = Thread(target=run_server)
    server_thread.start()

    log_thread = Thread(target=update_info_log)
    log_thread.start()


    server_thread.join()
    log_thread.join()
   

if __name__ == "__main__":
    main()
   