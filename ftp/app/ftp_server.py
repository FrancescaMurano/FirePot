import subprocess
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
import os

PORT = int(os.getenv("FTP_REAL_PORT", default="2121"))
PASSIVE_START_PORT = int(os.getenv("FTP_START_PORT",default="6000"))
PASSIVE_END_PORT = int(os.getenv("FTP_END_PORT",default="6006"))
MASQUERADE_ADDRESS = os.getenv("MASQUERADE_FTP_ADDRESS",default="127.0.0.1")

ADDRESS = '0.0.0.0'

# TRAP_PATH =  os.path.join(os.getcwd(),"ftp","app","home")
# DIRECTORY_PATH =  os.path.join(os.getcwd(),"ftp","app")

TRAP_PATH =  os.path.join(os.getcwd(),"app","home")
DIRECTORY_PATH =  os.path.join(os.getcwd(),"app")

#TRAP_PATH =  os.path.join(os.getcwd(),"home")
#DIRECTORY_PATH =  os.path.join(os.getcwd())

class LogHandler(logging.StreamHandler):
    def emit(self, record: logging.LogRecord) -> None:
        elastic = ElasticServer()

        if(record.getMessage().find("disconnect")) == -1:
            elastic.insert_data(FTPRequest(record.getMessage()).get_ftp_data_json())

        super().emit(record)

def restore_files():

    # Percorsi delle cartelle di origine e destinazione
    origin_dir = os.path.join(os.getcwd(),"app","files","home")
    remove_dir = os.path.join(os.getcwd(),"app","home")
    new_dir = os.path.join(os.getcwd(),"app")

    remove_p = ["rm","-r",remove_dir]
    cp_p = ["cp", "-r", origin_dir, new_dir]

    # Esegui il comando
    try:
        remove_process = subprocess.Popen(remove_p, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        copy_process = subprocess.Popen(cp_p, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    except Exception as e:
        print(str(e))


def remove_files_by_names(directory, filenames):

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
        self.insertion_blocked = False
        self.client_ip = ""
        self.port = ""
        self.banner = "ProFTPD 1.3.7"
        self.ftp_logger = logging.getLogger()
        self.ftp_logger.setLevel(logging.ERROR)
        self.ftp_logger.addHandler(LogHandler())

        self.elastic = ElasticServer()

    def _on_dtp_connection(self):
        self.client_ip = self.remote_ip
        self.client_port = self.remote_port
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

                msg = f"STOR: User {self.username} uploaded file {file_name}"
                logging.error(f"{self.client_ip}:{self.port}-[{self.username}] {msg} ")
                self.respond("226 Transfer complete.")
    
    def close(self):
        remove_files_by_names(TRAP_PATH, self.file_added)
        restore_files()
        self.elastic.insert_info_ip(get_ip_info(self.remote_ip))
        return super().close()

def main():
    authorizer = DummyAuthorizer()

    authorizer.add_user('root', 'root', TRAP_PATH, perm='elradfmwMT')
    authorizer.add_anonymous(TRAP_PATH)

    handler = MyFTPHandler
    handler.authorizer = authorizer
    address = (ADDRESS,PORT)
    server = FTPServer(address, handler)
    server.max_cons = 256
    server.max_cons_per_ip = 5
    server.handler.passive_ports = range(PASSIVE_START_PORT,PASSIVE_END_PORT)
    server.handler.active_dtp = MyActiveDTP
    server.handler.masquerade_address = MASQUERADE_ADDRESS

    server.serve_forever()

if __name__ == '__main__':
    main()
