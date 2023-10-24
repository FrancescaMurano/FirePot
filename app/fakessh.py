
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


s.bind(('0.0.0.0', 22))

s.listen(5)

while True:
    client_socket, client_address = s.accept()
    client_socket.send(b"SSH-2.0-OpenSSH-Server. Accesso limitato: Si prega di fornire credenziali valide o contattare l'amministratore di sistema.")
    # print(f"Connessione da: {client_address}")
    client_address_str = str(client_address)
    # message_bytes = f"Connessione da: {client_address_str} \n".encode('utf-8')
    # client_socket.send(message_bytes)
    client_socket.close()