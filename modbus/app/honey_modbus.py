

from threading import Thread
from modbus.server_slave import ServerSlave


def main():
    s = ServerSlave()
    t1 = Thread(target=s.run_server)
    t1.start()
   

if __name__ == "__main__":
    main()
   