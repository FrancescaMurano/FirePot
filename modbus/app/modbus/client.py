from pymodbus.client.sync import ModbusTcpClient
from pymodbus import *

# Client a scopo illustrativo per dimostrare il funzionamento del servizio MODBUS

SERVER = '34.17.52.4' # Insert Server IP
PORT = 502

client: ModbusTcpClient =  ModbusTcpClient(host=SERVER,port=PORT)
print (client)
# -------> read holding register
read_hr =  client.read_holding_registers(address=0, count=10,unit=0x01)
print("Holding register - ", read_hr.registers)

# write register

values = [0,0,0]
response = client.write_registers(address=0,values=values)


# read holding register
read_hr =  client.read_holding_registers(address=0, count=10,unit=0x01)

"""
    (1,3) =
    1 = Lettura con successo
    3 = numero di registri holding presenti nella risposta
"""
# -------> read coils register

read_co = client.read_coils(address=0,count=10,unit=0x01)
print("Coils: ", read_co.bits)

# -------> read input register

input_register = client.read_input_registers(address=0, count=10,unit=0x01)
print("input register: ", input_register.registers)


# -------> read discrete inputs register

discrete_in =  client.read_discrete_inputs(address=0, count=10, unit=0x01)
print("discrete_input: ", discrete_in.bits)



