import subprocess
import os
import re
from utils.utils_path import Path
ERROR = "Error: the sintax of the command is incorrect"

WHITELIST_COMMANDS = {
    "cd": ["cd keys","cd payments","cd users"],
    "ls": ["ls"],
    "cat": ["cat psw.txt", "cat credit_cards.json", "cat p_key.pkcs1", "cat user.txt"],
    "type": ["type psw.txt", "type credit_cards.json", "type p_key.pkcs1", "type user.txt"],
    "echo": ["echo"],
    "clear": ["clear"],
    "pwd": ["pwd"],
    "whoami": ["whoami"],
}

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

def exec_command(cmd: str):
    path = Path()
    output = ""
    error = ""
    if check_command(cmd):

        if cmd.startswith("cd"):
            destination =  cmd.split(" ")[1] if len(cmd.split(" ")) > 1  else ''
            path.set_current_path(os.path.join(path.get_start_full_path(),destination))
            result = subprocess.run(cmd, shell=True,cwd=path.get_start_full_path(), stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
            result.check_returncode()
            output = result.stdout.decode("utf-8")
            error = result.stderr.decode("utf-8")

        elif cmd.startswith("ls"):

            # to force the space elimination
            result = subprocess.run("ls", shell=True,cwd=path.get_current_path(), stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
            result.check_returncode()
            output = result.stdout.decode("utf-8")
            error = result.stderr.decode("utf-8")
        
        elif cmd.startswith("pwd"):
            output = "home"
            
        else:
            result = subprocess.run(cmd, shell=True,cwd=path.get_current_path(), stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
            result.check_returncode()
            output = result.stdout.decode("utf-8")
            error = result.stderr.decode("utf-8")

    else:
        if cmd.startswith("cd"):
            path.reset_path()
            result = subprocess.run("cd .", shell=True,cwd=path.get_current_path(), stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
            result.check_returncode()
            output = result.stdout.decode("utf-8")
            error = result.stderr.decode("utf-8")

        elif cmd.startswith("ls"):
            result = subprocess.run("ls", shell=True,cwd=path.get_current_path(), stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
            result.check_returncode()
            output = result.stdout.decode("utf-8")
            error = result.stderr.decode("utf-8")

        elif cmd.startswith("dir"):
            result = subprocess.run("dir", shell=True,cwd=path.get_current_path(), stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
            result.check_returncode()
            output = result.stdout.decode("utf-8")
            error = result.stderr.decode("utf-8")
        else:
            output = ERROR

    return (output,error)
