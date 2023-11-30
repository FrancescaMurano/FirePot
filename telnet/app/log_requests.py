from utils.utils_ip_info import get_ip_info
import datetime

class Request:

    # creo il file richieste
    def __init__(self, ip:str) -> None:
        self.ip = ""
        self.requests = []
        self.ip_info = get_ip_info(ip)

    def get_request_json(self,request: str):

        json_ip_request = {'ip': self.ip_info, 'command':request}
        json_ip_request["date"] =  datetime.datetime.now().isoformat()

        return json_ip_request
    
    def get_ip_info(self):
        return self.ip_info
        

    
