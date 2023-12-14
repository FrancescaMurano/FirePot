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

typer.echo("\
                \n██╗░░██╗░█████╗░███╗░░██╗███████╗██╗░░░██╗██████╗░░█████╗░████████╗  ██████╗░░░░░█████╗░\
                \n██║░░██║██╔══██╗████╗░██║██╔════╝╚██╗░██╔╝██╔══██╗██╔══██╗╚══██╔══╝  ╚════██╗░░░██╔══██╗\
                \n███████║██║░░██║██╔██╗██║█████╗░░░╚████╔╝░██████╔╝██║░░██║░░░██║░░░  ░█████╔╝░░░██║░░██║\
                \n██╔══██║██║░░██║██║╚████║██╔══╝░░░░╚██╔╝░░██╔═══╝░██║░░██║░░░██║░░░  ░╚═══██╗░░░██║░░██║\
                \n██║░░██║╚█████╔╝██║░╚███║███████╗░░░██║░░░██║░░░░░╚█████╔╝░░░██║░░░  ██████╔╝██╗╚█████╔╝\
                \n╚═╝░░╚═╝░╚════╝░╚═╝░░╚══╝╚══════╝░░░╚═╝░░░╚═╝░░░░░░╚════╝░░░░╚═╝░░░  ╚═════╝░╚═╝░╚════╝░")
    
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
        ftp_start_port: int = typer.Option(
            prompt = True,
            default = 6000,
            help = ""
        ),
        ftp_end_port: int = typer.Option(
            prompt = True,
            default = 6006,
            help = ""
        ),
        ftp_masquerade_address: str = typer.Option(
            prompt = True,
            default = "localhost",
            help = ""
        ),
        modbus_real_port: int = typer.Option(
            prompt = True,
            default = 5002,
            help = ""
        ),
        modbus_remote_port   : int = typer.Option(
            prompt = True,
            default = 502,
            help = ""
        ),
        elastic: bool = typer.Option(
            confirmation_prompt= True,
            default = True,
            help = ""
        ),

):
    
    with console.status("Loading..."):

        os.environ["SSH_REAL_PORT"] = str(ssh_real_port)
        os.environ["SSH_REMOTE_PORT"] = str(ssh_remote_port)

        os.environ["TELNET_REAL_PORT"] = str(telnet_real_port)
        os.environ["TELNET_REMOTE_PORT"] = str(telnet_remote_port)

        os.environ["MODBUS_REAL_PORT"] = str(modbus_real_port)
        os.environ["MODBUS_REMOTE_PORT"] = str(modbus_remote_port)

        os.environ["FTP_REAL_PORT"] = str(ftp_real_port)
        os.environ["FTP_REMOTE_PORT"] = str(ftp_remote_port)
        os.environ["FTP_START_PORT"] = str(ftp_start_port)
        os.environ["FTP_END_PORT"] = str(ftp_end_port)
        os.environ["FTP_MASQUERADE_ADDRESS"] = str(ftp_masquerade_address)


        if modbus:
            modbus_compose = "docker-compose_modbus.yml"
            command = f"docker-compose -f {modbus_compose} up -d"
            subprocess.run(command, shell=True)

        if ssh:
            ssh_compose = "docker-compose_ssh.yml"
            command = f"docker-compose -f {ssh_compose} up -d"
            subprocess.run(command, shell=True)

        if telnet:
            telnet_compose = "docker-compose_telnet.yml"
            command = f"docker-compose -f {telnet_compose} up -d"
            subprocess.run(command, shell=True)

        if ftp:    
            ftp_compose = "docker-compose_ftp.yml"
            command = f"docker-compose -f {ftp_compose} up -d"
            subprocess.run(command, shell=True)
        
        if elastic:
            elastic_compose = "docker-compose_kibana_elastic.yml"
            command = f"docker-compose -f {elastic_compose} up -d"
            subprocess.run(command, shell=True)

if __name__ == "__main__":
    typer.run(main)
