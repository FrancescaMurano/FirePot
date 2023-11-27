

from modbus.server_slave import ServerSlave


def main():
    s = ServerSlave()
    s.run_server()
   

if __name__ == "__main__":
    main()
   