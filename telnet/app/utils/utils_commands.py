import subprocess
import os
import re
from utils.utils_path import Path
ERROR_GEN = "Error: The sintax of the command is incorrect"
ERROR_PATH = "Error: The system cannot find the path specified."

WHITELIST_COMMANDS = {
    "cd": ["cd keys","cd payments","cd users"],
    "ls": ["ls","ls ../keys"],
    "dir": ["dir","dir ../keys"],
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
    error = ERROR_GEN
    if cmd == '' or cmd == None:
        return error
    else:
        if check_command(cmd):
            cmd = cmd.strip()
            error = "" 

            if cmd.startswith("cd"):
                destination =  cmd.split(" ")[1] if len(cmd.split(" ")) > 1  else ''
                result = subprocess.run(cmd, shell=True,cwd=path.get_current_path(), stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
                
                output = result.stdout.decode("utf-8")
                error = result.stderr.decode("utf-8")

                if error == "":
                    path.set_current_path(os.path.join(path.get_current_path(),destination))

            elif cmd.startswith("ls"):

                result = subprocess.run("ls", shell=True,cwd=path.get_current_path(), stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
                # result.check_returncode()
                output = result.stdout.decode("utf-8")
                error = result.stderr.decode("utf-8")
            
            elif cmd.startswith("pwd"):
                output = "home"
                
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

            elif cmd.startswith("ls"):
                result = subprocess.run("ls", shell=True,cwd=path.get_current_path(), stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
                # result.check_returncode()
                output = result.stdout.decode("utf-8")
                error = result.stderr.decode("utf-8")

            elif error == "":
                output = ERROR_GEN

    return (output,error)
