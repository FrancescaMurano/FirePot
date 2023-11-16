from utils.utils_ip_info import get_ip_info

class Requests:

    # creo il file richieste
    def __init__(self, ip:str) -> None:
        self.ip = ""
        self.requests = []
        self.ip_info = get_ip_info(ip)

    
    def add_request(self,request:str):
        self.requests.append(request)
    
    def get_requests(self):
        return self.requests
    
    def all_info_json(self):
        data = {
            'ip' : self.ip_info,
            'requests': self.requests
        }
        return data


    def get_ip_info(self):
        return self.ip_info

    
    
