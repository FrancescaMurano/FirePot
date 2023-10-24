# Script Python (esempio: socket_listener.py)

import socket

# Crea un socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Associa il socket a tutte le interfacce e alla porta 8083
s.bind(('0.0.0.0', 8083))

s.listen(5)

with open("richieste.txt", "ab") as file:
    while True:
        client_socket, client_address = s.accept()

        # print(f"Connessione da: {client_address}")

        client_socket.send(b"Benvenuto nel mio socket listener!\n")
        client_address_str = str(client_address)

        # Creare il messaggio come un oggetto di tipo bytes
        message_bytes = f"Connessione da: {client_address_str} \n".encode('utf-8')
        client_socket.send(message_bytes)
        file.write(message_bytes)

        file.flush()

        client_socket.close()
