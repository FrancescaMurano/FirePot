import subprocess
import typer
from typer import Typer, Option, style
from requests import Session
from rich.console import Console
import os
import requests

app = Typer()
session = Session()
console = Console(record=True)

def upload_dash(ip: str):
    DASHBOARD_FTP_FILE="dashboards/ftp_dashboard.ndjson"
    DASHBOARD_SSH_FILE="dashboards/modbus_dashboard.ndjson"
    DASHBOARD_TELNET_FILE="dashboards/ssh_dashboard.ndjson"
    DASHBOARD_MODBUS_FILE="dashboards/telnet_dashboard.ndjson"

    KIBANA_API_URL="http://${KIBANA_HOST}:${KIBANA_PORT}/api/saved_objects/_import"

    KIBANA_HOST = ip
    KIBANA_PORT = 5601

    KIBANA_API_URL = f"http://{KIBANA_HOST}:{KIBANA_PORT}/api/saved_objects/_import"

    ftp_response = requests.post(
        KIBANA_API_URL,
        headers={"kbn-xsrf": "true"},
        files={"file": open(DASHBOARD_FTP_FILE, "rb")},
    )

    ssh_response = requests.post(
        KIBANA_API_URL,
        headers={"kbn-xsrf": "true"},
        files={"file": open(DASHBOARD_SSH_FILE, "rb")},
    )

    modbus_response = requests.post(
        KIBANA_API_URL,
        headers={"kbn-xsrf": "true"},
        files={"file": open(DASHBOARD_MODBUS_FILE, "rb")},
    )

    telnet_response = requests.post(
        KIBANA_API_URL,
        headers={"kbn-xsrf": "true"},
        files={"file": open(DASHBOARD_TELNET_FILE, "rb")},
    )

    print("FTP Dashboard Import Response:", ftp_response.text)
    print("SSH Dashboard Import Response:", ssh_response.text)
    print("Modbus Dashboard Import Response:", modbus_response.text)
    print("Telnet Dashboard Import Response:", telnet_response.text)




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
            prompt = f"Do you want to start a {style('TELNET', fg='green')} honeypot? Press Y or N.",
            help = f"Start a {style('TELNET', fg='green')} honeypot. Press Y = yes, N = no"
        ),
        ssh: bool = typer.Option(
            default = True,
            prompt = f"Do you want to start a {style('SSH', fg='yellow')} honeypot? Press Y or N.",
            help = f"Start a {style('SSH', fg='yellow')} honeypot. Press Y = yes, N = no"
        ),
        modbus: bool = typer.Option(
            default = True,
            prompt = f"Do you want to start a {style('MODBUS', fg='red')} honeypot? Press Y or N.",
            help = f"Start a {style('MODBUS', fg='red')} honeypot. Press Y = yes, N = no"

        ),
        ftp: bool = typer.Option(
            default = True,
            prompt = f"Do you want to start a {style('FTP', fg='magenta')} honeypot? Press Y or N.",
            help = f"Start a {style('FTP', fg='magenta')} honeypot. Press Y = yes, N = no"
        ),
        telnet_real_port: int = typer.Option(
            prompt = f"Insert the real port of your {style('TELNET', fg='green')} honeypot (Skip if you don't start the service).",
            default = 2323,
            help = f"The rel port on which the {style('TELNET', fg='green')} service will be executed"
        ),
        telnet_remote_port: int = typer.Option(
            prompt = f"Choice the remote port of {style('TELNET', fg='green')} service (Skip if you don't start the service).",
            default = 23,
            help = f"The remote port on which the {style('TELNET', fg='green')} service will be executed, the externally detected port."
        ),
        ssh_real_port: int = typer.Option(
            prompt = f"Choice the real port of SSH service (Skip if you don't start the service).",
            default = 2222,
            help = f"The real port on which the SSH service will be executed."
        ),
        ssh_remote_port: int = typer.Option(
            prompt = f"Choice the remote port of SSH service (Skip if you don't start the service).",
            default = 22,
            help = f"The remote port on which the SSH service will be executed, the externally detected port."
        ), 
        ftp_real_port: int = typer.Option(
            prompt = f"Choice the real port of {style('FTP', fg='magenta')} service (Skip if you don't start the service)",
            default = 2121,
            help = f"The real port on which the {style('FTP', fg='magenta')} service will be executed."
        ),
        ftp_remote_port: int = typer.Option(
           prompt = f"Choice the remote port of {style('FTP', fg='magenta')} service (Skip if you don't start the service).",
            default = 21,
            help = f"The remote port on which the {style('FTP', fg='magenta')} service will be executed, the externally detected port."
        ),
        ftp_start_port: int = typer.Option(
            prompt = f"Choice the starting range port for {style('FTP', fg='magenta')} passive communication (Skip if you don't start the service).",
            default = 6000,
            help = f"The starting range for {style('FTP', fg='magenta')} passive communication."
        ),
        ftp_end_port: int = typer.Option(
            prompt = f"Choice the ending range port for {style('FTP', fg='magenta')} passive communication (Skip if you don't start the service).",
            default = 6006,
            help = f"The endig range for {style('FTP', fg='magenta')} passive communication."
        ),
        ftp_masquerade_address: str = typer.Option(
            prompt = f"Choice the masquerade address for {style('FTP', fg='magenta')} service (Skip if you don't start the service).",
            default = "localhost",
            help = f"External IP visible to users outside the firewall."
        ),
        modbus_real_port: int = typer.Option(
            prompt = f"Choice the real port of {style('MODBUS', fg='red')} service (Skip if you don't start the service)",
            default = 5002,
            help = f"The real port on which the {style('MODBUS', fg='red')} service will be executed."
        ),
        modbus_remote_port   : int = typer.Option(
            prompt = f"Choice the remote port of {style('MODBUS', fg='red')} service (Skip if you don't start the service)",
            default = 502,
            help = f"The remote port on which the {style('MODBUS', fg='red')} service will be executed, the externally detected port."
        ),
        elastic_kibana: bool = typer.Option(
            prompt = f"Do you want to start here an ElasticSearch service? Press Y or N.",
            default = True,
            help = f"Press Y to init Elasticsearch and Kibana locally in your machine. Press N if you have already this instances in another machine. \
            Pay attention, elasticsearch/kibana is mandatory for the correct functioning of this tool."
        ),
        ip_elastic_kibana: str = typer.Option(
            prompt = f"Insert the IP ADDRESS of the elastic instance.",
            default = "localhost",
            help = f"Public IP address of ElasticSearch instance."
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
        
        os.environ["IP_ELASTIC_KIBANA"] = str(ip_elastic_kibana)


        if modbus:
            modbus_compose = "docker-compose_modbus.yml"
            command = f"docker-compose -f {modbus_compose} up  -d --build"
            subprocess.run(command, shell=True)

        if ssh:
            ssh_compose = "docker-compose_ssh.yml"
            command = f"docker-compose -f {ssh_compose} up  -d --build"
            subprocess.run(command, shell=True)

        if telnet:
            telnet_compose = "docker-compose_telnet.yml"
            command = f"docker-compose -f {telnet_compose} up  -d --build"
            subprocess.run(command, shell=True)

        if ftp:    
            ftp_compose = "docker-compose_ftp.yml"
            command = f"docker-compose -f {ftp_compose} up  -d --build"
            subprocess.run(command, shell=True)
        
        if elastic_kibana:
            elastic_compose = "docker-compose_kibana_elastic.yml"
            command = f"docker-compose -f {elastic_compose} up  -d"
            try:
                process = subprocess.run(command, shell=True)
            except Exception as e:
                print(str(e))
            finally:
                upload_dash(ip=os.environ["IP_ELASTIC_KIBANA"])

if __name__ == "__main__":
    typer.run(main)
