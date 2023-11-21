from pymodbus.server.async_io import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext

ADDR = "0.0.0.0"
PORT = 502

# Slave creation with common register (discrete inputs, coils, holding register, input register)
store = ModbusSlaveContext( 
    di = ModbusSequentialDataBlock(0, [7]*100),
    co = ModbusSequentialDataBlock(0, [1]*100),
    hr = ModbusSequentialDataBlock(0, [9]*100),
    ir = ModbusSequentialDataBlock(0, [6]*100))

# Server Context Creation
context = ModbusServerContext(slaves=store, single=False)

# Start
StartTcpServer(context = context, address=(ADDR, PORT))