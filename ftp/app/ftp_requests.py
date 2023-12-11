import datetime
import re
from utils.utils_ip_info import get_ip_info

class FTPRequest:

    def __init__(self, request: str) -> None:

        self.date = ""
        self.ip= ""
        self.port = ""
        self.name = ""
        self.message= ""
        print(request)

        reg = r'(?P<ip>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})|(::\d{1,5})):(?P<port>\d{0,5})-\[(?P<name>[A-Za-z0.-9]*)\]\s(?P<message>.*)'
        
        search = re.search(reg,request)

        if search != None:
            self.date =  datetime.datetime.now().isoformat(),
            self.ip = search.group("ip")
            self.port = search.group("port")
            self.name = search.group("name")
            self.message = search.group("message")
    
    def get_ftp_data_json(self):
        data = get_ip_info(self.ip)
        data['time'] = self.date
        data['port'] = self.port
        data['name'] = self.name
        data['message'] = self.message

        return data
