import os
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import logging

PORT = 21
ADDRESS = ''
TRAP_PATH =  os.path.join(os.getcwd(),"ftp","app","home")
DIRECTORY_PATH =  os.path.join(os.getcwd(),"ftp","app")


def remove_files_by_names(directory, filenames):
    """
    Rimuove i file con i nomi specificati dalla directory.
    """
    for filename in filenames:
        file_path = os.path.join(directory, filename)
        try:
            os.remove(file_path)
            print(f"File '{filename}' rimosso con successo.")
        except FileNotFoundError:
            print(f"File '{filename}' non trovato.")
        except Exception as e:
            print(f"Errore durante la rimozione di '{filename}': {e}")

class MyFTPHandler(FTPHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_added = []
        self.log_directory = DIRECTORY_PATH  # Sostituisci con il percorso desiderato
        self.log_file_path = os.path.join(self.log_directory, "ftp_actions.log")
        self.insertion_blocked = False
        self.client_ip = ""

        logging.basicConfig(
            filename=self.log_file_path,
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s]: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    def log_action(self, ip_address,action_message):
        logging.info(f"{ip_address} - {action_message}")
    
    def _on_dtp_connection(self):
        self.client_ip = self.remote_ip
        return super()._on_dtp_connection()
    

    def ftp_STOR(self, file, mode='w'):

            if self.insertion_blocked:
                self.respond("554 Permission denied. Insertion is blocked.")
            else:
                file_name  = os.path.basename(file)
                self.file_added.append(file_name)
                name = os.path.join(os.getcwd(),"ftp","app","home",file_name)

                with open(name, 'w') as error_file:
                    error_file.write("Error, file corrupted")

                self.log_action(action_message=f"STOR: User {self.username} uploaded file {file_name}",ip_address=self.client_ip)
                self.respond("226 Transfer complete.")
    
    def close(self):
        remove_files_by_names(TRAP_PATH, self.file_added)
        return super().close()

def main():
    authorizer = DummyAuthorizer()

    authorizer.add_user('user', '12345',os.path.join(os.getcwd(),"ftp","app","home"), perm='elradfmwMT')
    authorizer.add_anonymous(os.path.join(os.getcwd(),"ftp","app","home"))

    handler = MyFTPHandler
    handler.authorizer = authorizer
    handler.banner = "pyftpdlib based ftpd ready."

    address = (ADDRESS,PORT)
    server = FTPServer(address, handler)

    server.max_cons = 256
    server.max_cons_per_ip = 5

    # start ftp server
    server.serve_forever()

if __name__ == '__main__':
    main()