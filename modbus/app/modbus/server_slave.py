from pymodbus.server.asynchronous import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
from pymodbus.device import ModbusDeviceIdentification
import logging,logging.handlers
from elastic.elasticserver import ElasticServer
import os
from modbus.modbus_request import ModbusConnectionRequest,ModbusRequest
from pygtail import Pygtail

ADDR = "0.0.0.0"
PORT = 5002

FORMAT = ('%(asctime)-15s %(message)s')
log_path = os.path.join("app","modbus","log_file.log")
logging.basicConfig(filename=log_path,format=FORMAT,datefmt='%Y-%m-%d %H:%M:%S')
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().handlers[0].flush()

class ServerSlave:
    def __init__(self) -> None:
        self.elastic = ElasticServer()
        
        # Slave creation with common register (discrete inputs, coils, holding register, input register)
        store = ModbusSlaveContext( 
            di = ModbusSequentialDataBlock(0, [0]*100),
            co = ModbusSequentialDataBlock(0, [1]*100),
            hr = ModbusSequentialDataBlock(0, [0]*100),
            ir = ModbusSequentialDataBlock(0, [1]*100))

        self.identity = ModbusDeviceIdentification()
        self.identity.VendorName = 'PM710 PowerMeter'
        self.identity.ModelName = 'Schneider Electric PM710 v03.110'
        self.identity.ProductCode = 'PM710'

        # Server Context Creation
        self.context = ModbusServerContext(slaves=store, single=True)

    def read_file(self):
        try:
            for line in Pygtail(log_path):
                lines = line.split("\r\n")
                for l in lines:
                    if l.find("Client Connected") != -1:
                        r1 = ModbusConnectionRequest(l)
                        self.elastic.insert_modbus_connection_request(r1.get_json())
                    else:
                        r2 = ModbusRequest(l)
                        self.elastic.insert_modbus_log_request(r2.get_json())
        except Exception as e:
            print("Error")

    def run_server(self):
        StartTcpServer(context = self.context,identity=self.identity, address=(ADDR, PORT))
