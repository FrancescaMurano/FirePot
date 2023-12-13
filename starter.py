class UserInput:
    PORT_SSH_REMOTE = 22
    PORT_SSH_REAL = 2222

    PORT_TELNET_REMOTE = 23
    PORT_TELNET_REAL = 2323

    PORT_MODBUS_REMOTE = 502
    PORT_MODBUS_REAL = 5002

    PORT_FTP_REMOTE = 21
    PORT_FTP_REAL = 2121

    IP_ADDRESS = "localhost"
    FTP_PASSIVE_PORT_START = 6000
    FTP_PASSIVE_PORT_END = 6006

# 1. docker compose up --> elastic e kibana
# 2. POST delle dashboard
# 3. scelta degli honeypot da utilizzare (SSH,TELNET,MODBUS,FTP)
# 4. apertura delle porte -- abilitazione porte su iptables
# 5. scelta delle porte
# 6. docker con le porte scelte 
# 7. Menu:
#   - Visualizza dashboard
#   - exit and down
#   - exit 


import subprocess
import time
import typer
from requests import ConnectTimeout, HTTPError, ReadTimeout, Session, Timeout
from rich.markup import escape
from rich.console import Console
from urllib3.exceptions import NewConnectionError
import os

app = typer.Typer()
session = Session()
console = Console(record=True)



@app.callback()
def main(
        telnet: bool = typer.Option(
            default = True,
            prompt = True,
            help = ""
        ),
        ssh: bool = typer.Option(
            default = True,
            prompt = True,
            help = ""
        ),
        modbus: bool = typer.Option(
            prompt = True,
            default = True,
            help = ""

        ),
        ftp: bool = typer.Option(
            prompt = True,
            default = True,
            help = ""
        ),
        telnet_real_port: int = typer.Option(
            prompt = True,
            default = 2323,
            help = ""
        ),
        telnet_remote_port: int = typer.Option(
            prompt = True,
            default = 23,
            help = ""
        ),
        ssh_real_port: int = typer.Option(
            prompt = True,
            default = 2222,
            help = ""
        ),
        ssh_remote_port: int = typer.Option(
            prompt = True,
            default = 22,
            help = ""
        ), 
        ftp_real_port: int = typer.Option(
            prompt = True,
            default = 2121,
            help = ""
        ),
        ftp_remote_port: int = typer.Option(
            prompt = True,
            default = 21,
            help = ""
        ),
        modbus_real_port: int = typer.Option(
            prompt = True,
            default = 502,
            help = ""
        ),
        modbus_remote_port   : int = typer.Option(
            prompt = True,
            default = 5002,
            help = ""
        ),    

):
    with console.status("Loading..."):
        parameters = locals()
        elastic_kibana_path =  os.path.join(os.getcwd(),"docker-compose_elastic_kibana.yml")
        honey_path =  os.path.join(os.getcwd(),"docker-compose_ssh.yml")

        # Imposta le variabili d'ambiente
        variable = f"export VALORE1=${ssh_real_port}"
        subprocess.run(variable, shell=True)
        # Esegui Docker Compose
        docker_compose_command = f"docker-compose -f {honey_path} build && docker-compose -f {honey_path} -f {elastic_kibana_path} up -d"
        subprocess.run(docker_compose_command, shell=True)

if __name__ == "__main__":
    typer.run(main)
