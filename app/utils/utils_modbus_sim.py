# Lettura di registri digitali (Function Code 2):

REQUEST_FUNCTION_02 = " \
    Transaction ID: 0x0003\n \
    Protocol ID: 0x0000\n \
    Length: 0x0006\n \
    Unit ID: 0x01\n \
    Function Code: 0x02\n \
    Starting Address: 0x0000\n \
    Quantity of Coils: 0x0004\n "

# Lettura di registri analogici (Function Code 3):
REQUEST_FUNCTION_03 = "Transaction ID: 0x0001\n \
    Protocol ID: 0x0000\n  \
    Length: 0x0006\n \
    Unit ID: 0x01\n \
    Function Code: 0x03\n \
    Starting Address: 0x0000\n \
    Quantity of Registers: 0x0002\n"


# Scrittura di uno stato di uscita digitale (Function Code 5):
REQUEST_FUNCTION_05 = " \
    Transaction ID: 0x0004\n \
    Protocol ID: 0x0000\n \
    Length: 0x0006\n \
    Unit ID: 0x01\n \
    Function Code: 0x05\n \
    Output Address: 0x0001\n \
    Output Value: 0xFF00\n"

# Scrittura di un registro analogico (Function Code 6):
REQUEST_FUNCTION_06 = "Transaction ID: 0x0002\n \
    Protocol ID: 0x0000\n \
    Length: 0x0006\n \
    Unit ID: 0x01\n \
    Function Code: 0x06\n \
    Address: 0x0000\n \
    New Value: 0x5678\n"

ERROR = "Error! Command not recognized.\n"

def simulate_response_03():
    return "Transaction ID: 0x0001\n \
    Protocol ID: 0x0000\n\
    Length: 0x0007\n\
    Unit ID: 0x01\n\
    Function Code: 0x03\n\
    Byte Count: 0x04\n\
    Register Values: 0x1234 0xABCD\n"

def simulate_response_04():
    return "Transaction ID: 0x0002\n \
    Protocol ID: 0x0000\n \
    Length: 0x0006\n \
    Unit ID: 0x01\n \
    Function Code: 0x06\n \
    Address: 0x0000\n \
    New Value: 0x5678\n"

def simulate_response_05():
    return " \
    Transaction ID: 0x0004\n \
    Protocol ID: 0x0000\n \
    Length: 0x0006\n \
    Unit ID: 0x01\n \
    Function Code: 0x05\n \
    Output Address: 0x0001\n \
    Output Value: 0xFF00\n"

def simulate_response_06():
    return " \
    Transaction ID: 0x0003\n \
    Protocol ID: 0x0000\n \
    Length: 0x0005\n \
    Unit ID: 0x01\n \
    Function Code: 0x02\n \
    Byte Count: 0x01\n \
    Coil Status: 0x0F\n"

def hex_to_big_endian(hex_string):
    return bytearray.fromhex(hex_string)

def return_type(req: str):
    hex_string = ""
    req = req.replace(" ","")
    if len(req) > 4:
        hex_string = f"{req[2]}{req[3]}"
    return hex_string