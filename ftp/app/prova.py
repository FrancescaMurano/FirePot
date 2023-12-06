from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

def on_stor_handler(conn, file_path, callback=None):
    """
    Gestisce l'evento STOR (inserimento).
    Puoi inserire qui la tua logica di controllo dell'inserimento.
    """
    print("PROVA STORE")
    # Esempio: Blocca l'inserimento e restituisci un messaggio di successo
    conn.respond("550 Permission denied. Insertion is blocked.")

# Crea un authorizer con un utente anonimo e un utente con credenziali
authorizer = DummyAuthorizer()
authorizer.add_anonymous(".")
authorizer.add_user("root", "root", ".", perm="elradfmw")

# Crea un gestore FTP personalizzato
handler = FTPHandler
handler.on_stor = on_stor_handler  # Assegna la funzione di gestione STOR

# Crea il server FTP
server = FTPServer(("127.0.0.1", 21), handler)
server.authorizer = authorizer

# Avvia il server FTP
server.serve_forever()
