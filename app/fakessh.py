
# import socket

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# s.bind(('0.0.0.0', 22))

# s.listen(5)

# while True:
#     client_socket, client_address = s.accept()
#     client_socket.send(b"SSH-2.0-OpenSSH-Server. Accesso limitato: Si prega di fornire credenziali valide o contattare l'amministratore di sistema.")
#     # print(f"Connessione da: {client_address}")
#     client_address_str = str(client_address)
#     # message_bytes = f"Connessione da: {client_address_str} \n".encode('utf-8')
#     # client_socket.send(message_bytes)
#     client_socket.close()
import threading
import paramiko
import socket

# Crea una classe per gestire le connessioni SSH
class SSHServer(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        # Implementa l'autenticazione dell'utente
        if username == "tuoutente" and password == "tupassword":
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

# Crea un socket per il server SSH
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 22))  # Ascolta sulla porta 22

server_socket.listen(5)

print("In attesa di connessioni SSH...")

while True:
    client_socket, addr = server_socket.accept()

    transport = paramiko.Transport(client_socket)
    transport.add_server_key()
    
    server = SSHServer()
    transport.start_server(server=server)

    print(f"Connessione da {addr[0]}:{addr[1]}")

    channel = transport.accept(20)
    if channel is None:
        print("Nessuna sessione creata.")
        transport.close()
        
        break

    # Leggi e scrivi dati sulla sessione del canale SSH
    while True:
        try:
            command = channel.recv(1024)
            if not command:
                break
            output = f"Comando ricevuto: {command.decode()}"
            channel.send(output)
        except Exception as e:
            print(f"Errore: {str(e)}")
            break

    channel.close()
    transport.close()
