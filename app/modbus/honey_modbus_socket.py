import socket

# from modbus.modbus_response import ModbusResponse
from modbus.modbus_response_socket import *

HOST = '127.0.0.1'
PORT = 502

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()

    if conn is not None:
        conn.send("> ".encode("utf-8"))
    while True:
        client_address_str = str(addr[0]).encode("utf-8")
        data = conn.recv(1024)
        if not data:
            break
        if data == b'exit\n':
            conn.close()
            break

        r = ModbusResponse(data)
        conn.send(r.get_response())
        conn.send("> ".encode("utf-8"))

        print(data)

    s.close()
