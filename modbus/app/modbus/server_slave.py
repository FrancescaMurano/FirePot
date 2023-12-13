from logging import LogRecord
from pymodbus.server.asynchronous import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
from pymodbus.device import ModbusDeviceIdentification
import logging,logging.handlers
from elastic.elasticserver import ElasticServer
from modbus.modbus_request import ModbusRequest
from utils.utils_ip_info import get_ip_info
from twisted.internet import protocol
import os

ADDR = "0.0.0.0"
PORT = int(os.getenv("MODBUS_REAL_PORT",default="5002"))

class ConnectionLogHandler(logging.StreamHandler):
    
    def emit(self, record: LogRecord) -> None:
        server = ElasticServer()
        log_message = self.format(record)
        
        if "Client Connected" in log_message:
            super().emit(record)

        elif "Data Received" in log_message or "Factory Request" in log_message:
            r2 = ModbusRequest(record.getMessage())
            server.insert_modbus_log_request(r2.get_json())
            super().emit(record)

pymodbus_logger = logging.getLogger("pymodbus")

pymodbus_logger.setLevel(logging.DEBUG)

pymodbus_logger.addHandler(ConnectionLogHandler())

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

    def run_server(self):
        StartTcpServer(context = self.context,identity=self.identity, address=(ADDR, PORT))
