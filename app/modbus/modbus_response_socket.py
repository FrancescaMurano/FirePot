

from utils.utils_modbus_sim import *

VALID = ["02","03","05","06"]

class ModbusResponse:

    def __init__(self, req: bytes) -> None:
        self.request = req.decode("utf-8")
        self.type  = return_type(req=self.request)

    def get_response(self):
        match self.type:
            case "02":
                return REQUEST_FUNCTION_02.encode("utf-8")
            case "03":
                return REQUEST_FUNCTION_03.encode("utf-8")
            case "05":
                return REQUEST_FUNCTION_05.encode("utf-8")
            case "06":
                return REQUEST_FUNCTION_06.encode("utf-8")
            case _:
                return ERROR.encode("utf-8")