import datetime
import re

class FTPRequest:

    def __init__(self, request: str) -> None:

        self.date = ""
        self.ip= ""
        self.port = ""
        self.name = ""
        self.message= ""
        print(request)

        reg = r'(?P<ip>(\d{1,3}+\.\d{1,3}+\.\d{1,3}+\.\d{1,3}+)|(::\d+)):(?P<port>\d{1,5})-\[(?P<name>[A-Za-z0.-9]+)\]\s(?P<message>.*)'
        
        search = re.search(reg,request)

        if search != None:
            self.date =  datetime.datetime.now().isoformat(),
            self.ip = search.group("ip")
            self.port = search.group("port")
            self.name = search.group("name")
            self.message = search.group("message")
    
    def get_ftp_data_json(self):
        return {
            'time':  self.date ,
            'ip':    self.ip,
            'port':  self.port,
            'name':  self.name,
            'message':self.message,
        }
