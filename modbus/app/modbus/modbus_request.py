import re
import datetime

class ModbusRequest:
    def __init__(self, request: str) -> None:
        print(request)
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
    
