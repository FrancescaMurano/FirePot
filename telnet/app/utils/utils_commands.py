import subprocess
import os
import re
from .commands import *
from utils.utils_path import Path


def check_command(cmd: str):
    echo_pattern = r'^echo\s+[A-Za-z0-9\s]+$'
    found = False

    for command in WHITELIST_COMMANDS.keys():
        if re.match(echo_pattern, cmd):
            found = True
            break
        if cmd in WHITELIST_COMMANDS[command]:
            found = True
            break

    return found

def exec_command(cmd: str, path:Path):
    output = ""
    error = ERROR_GEN
    
    if cmd == '' or cmd == None:
        return error
    else:
        if check_command(cmd):
            cmd = cmd.strip()
            error = ""
            output = "" 

            if cmd.startswith("cd"):
                destination =  cmd.split(" ")[1] if len(cmd.split(" ")) > 1  else ''
                result = subprocess.run(cmd, shell=True,cwd=path.get_current_path(), stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
                
                output = result.stdout.decode("utf-8")
                error = result.stderr.decode("utf-8")

                if error == "":
                    destination = re.search(r"[a-zA-Z]+",destination).group()
                    path.set_current_path(os.path.join(path.get_current_path(),destination))

            elif cmd == "ifconfig":
                output = IFCONFIG_SIMPLE_RESPONSE

            elif cmd == "ifconfig -a":
                output = IFCONFIG_FULL_RESPONSE
            
            elif cmd == "ip a":
                output = IP_A_RESPONSE
                
            elif cmd.startswith("ls"):
                result = subprocess.run(cmd, shell=True,cwd=path.get_current_path(), stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
                # result.check_returncode()
                output = result.stdout.decode("utf-8")
                error = result.stderr.decode("utf-8")
            
            elif cmd.startswith("pwd"):
                output = "home"

            elif cmd.startswith("id"):
                output = "uid=0(root) gid=0(root) gruppi=0(root)"
            
            else:
                result = subprocess.run(cmd, shell=True,cwd=path.get_current_path(), stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
                # result.check_returncode()
                output = result.stdout.decode("utf-8")
                error = result.stderr.decode("utf-8")
        else:
            if cmd.startswith("cd") and cmd.find("..")!=-1:
                path.reset_path()
                result = subprocess.run("cd .", shell=True,cwd=path.get_current_path(), stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
                # result.check_returncode()
                output = result.stdout.decode("utf-8")
                error = result.stderr.decode("utf-8")

            elif cmd.startswith("cd") and cmd.find("..")==-1:
                output = ERROR_PATH

            # elif cmd.startswith("ls"):
            #     result = subprocess.run("ls", shell=True,cwd=path.get_current_path(), stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
            #     # result.check_returncode()
            #     output = result.stdout.decode("utf-8")
            #     error = result.stderr.decode("utf-8")

            elif error == "":
                output = ERROR_GEN

    return (output,error)
