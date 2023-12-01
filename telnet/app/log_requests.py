from utils.utils_ip_info import get_ip_info
import datetime

class Request:

    # creo il file richieste
    def __init__(self, ip:str) -> None:
        self.ip = ""
        self.requests = []
        self.info = get_ip_info(ip)
        self.ip = get_ip_info(ip)

    def get_request_json(self,request: str):

        self.info['command'] = request
        self.info["date"] =  datetime.datetime.now().isoformat()

        return self.info
    
    def get_ip_info(self):
        return self.ip
        

    
