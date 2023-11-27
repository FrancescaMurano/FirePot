import re

class ModbusConnectionRequest:
    def __init__(self, request: str) -> None:

        self.ip   = ""
        self.port = ""
        self.data = ""
        self.time = ""

        reg_data = '(?P<data>\d{4}-\d{2}-\d{2})\s(?P<time>\d{2}:\d{2}:\d{2})'
        reg_ip = '(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        reg_port = 'port=(?P<port>\d{1,5})'

        ip_search = re.search(reg_ip,request)
        port_search = re.search(reg_port,request)
        data_search = re.search(reg_data,request)

        if ip_search != None and port_search!=None and data_search!=None:
            self.ip = ip_search.group("ip")
            self.port = port_search.group("port")
            self.data = data_search.group("data")
            self.time = data_search.group("time")
    
    def get_json(self):

        return {
            'data':self.data,
            'time':self.time,
            'ip':  self.ip,
            'port':self.port,
        }
    
class ModbusRequest:
    def __init__(self, request: str) -> None:

        self.data = ""
        self.time = ""
        self.message = ""

        reg = '(?P<data>\d{4}-\d{2}-\d{2})\s(?P<time>\d{2}:\d{2}:\d{2})\s+(?P<msg>.+)'

        search = re.search(reg,request)

        if search != None:
            self.data = search.group("data")
            self.time = search.group("time")
            self.message = search.group("msg")
    
    def get_json(self):
        return {
            'data':self.data,
            'time':self.time,
            'msg':self.message,
        }
    
