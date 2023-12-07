import asyncio
import os
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import logging
from pyftpdlib.handlers import PassiveDTP,ActiveDTP
from elastic.elasticserver import ElasticServer
from ftp_requests import FTPRequest
from utils.utils_ip_info import get_ip_info

PORT = 2121
ADDRESS = ''

# TRAP_PATH =  os.path.join(os.getcwd(),"ftp","app","home")
# DIRECTORY_PATH =  os.path.join(os.getcwd(),"ftp","app")

# TRAP_PATH =  os.path.join(os.getcwd(),"app","home")
# DIRECTORY_PATH =  os.path.join(os.getcwd(),"app")

## PATH FOR DOCKER CONTAINER
TRAP_PATH =  os.path.join(os.getcwd(),"home")
DIRECTORY_PATH =  os.path.join(os.getcwd())

class LogHandler(logging.StreamHandler):
    def emit(self, record: logging.LogRecord) -> None:
        elastic = ElasticServer()
        print(FTPRequest(record.getMessage()).get_ftp_data_json())
        if(record.getMessage().find("disconnect")) != -1:
            elastic.insert_data(FTPRequest(record.getMessage()).get_ftp_data_json())

        super().emit(record)


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

class MyActiveDTP(ActiveDTP):
    def __init__(self, inst, *args, **kwargs):
        super().__init__(inst, *args, **kwargs)
        self.port = 6006  # Imposta la porta attiva desiderata

class MyFTPHandler(FTPHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.file_added = []
        self.log_directory = DIRECTORY_PATH  # Sostituisci con il percorso desiderato
        self.log_file_path = os.path.join(self.log_directory, "ftp_actions.log")
        self.insertion_blocked = False
        self.client_ip = ""

        ftp_logger = logging.getLogger()
        ftp_logger.setLevel(logging.ERROR)
        ftp_logger.addHandler(LogHandler())

        self.elastic = ElasticServer()


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
                name = os.path.join(TRAP_PATH,file_name)

                with open(name, 'w') as error_file:
                    error_file.write("Error, file corrupted")

                self.log_action(action_message=f"STOR: User {self.username} uploaded file {file_name}",ip_address=self.client_ip)
                self.respond("226 Transfer complete.")
    
    def close(self):
        remove_files_by_names(TRAP_PATH, self.file_added)
        self.elastic.insert_info_ip(get_ip_info(self.remote_ip))
        return super().close()

def main():
    authorizer = DummyAuthorizer()

    authorizer.add_user('user', '12345', TRAP_PATH, perm='elradfmwMT')
    authorizer.add_anonymous(TRAP_PATH)

    handler = MyFTPHandler
    handler.authorizer = authorizer
    handler.banner = "pyftpdlib based ftpd ready."

    address = (ADDRESS,PORT)
    server = FTPServer(address, handler)
    server.max_cons = 256
    server.max_cons_per_ip = 5
    server.handler.passive_ports = range(6000, 6006)
    server.handler.active_dtp = MyActiveDTP
    server.handler.masquerade_address = "0.0.0.0"

    server.serve_forever()

if __name__ == '__main__':
    main()
