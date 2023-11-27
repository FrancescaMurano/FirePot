import re
import datetime

class ModbusConnectionRequest:
    def __init__(self, request: str) -> None:

        self.ip   = ""
        self.port = ""
        self.date = ""
        self.time = ""

        reg_ip = '(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        reg_port = 'port=(?P<port>\d{1,5})'

        ip_search = re.search(reg_ip,request)
        port_search = re.search(reg_port,request)

        if ip_search != None and port_search!=None:
            self.ip = ip_search.group("ip")
            self.port = port_search.group("port")
            self.date = datetime.datetime.now().isoformat()

    def get_ip(self):
        return self.ip
    
    def get_json(self):

        return {
            'date':self.date,
            'ip':  self.ip,
            'port':self.port,
        }
    
class ModbusRequest:
    def __init__(self, request: str) -> None:

        self.date = datetime.datetime.now().isoformat()

        reg1 = '(?P<type>Data\sReceived):\s(?P<request>.+)'
        reg2 = '(?P<type>Factory\sRequest)\[(?P<request>[A-Za-z]+)'

        search1 = re.search(reg1,request)
        search2 = re.search(reg2,request)


        if search1 != None:
            self.type = search1.group("type")
            self.request = search1.group("request")
            
        elif search2 != None:
            self.type = search2.group("type")
            self.request = search2.group("request")
    
    def get_json(self):
        return {
            'date': self.date,
            'type': self.type,
            'request':self.request,
        }
    
