from pymodbus.client import ModbusTcpClient
import os


PLC_IP = "192.168.10.10"
PORT = 502

COILS = {
    "full": 16384,
    "robot_moving": 16385,
    "photoeye": 16386,
    "auto_mode": 16387,
    "enable": 16388,
}

PART_COUNT_REGISTER = 49152

def get_state(coils):
    if coils["robot_moving"]:
        return "ROBOT MOVING"
    elif coils["full"]:
        return "STOPPED: REQUIRE PICKUP"
    elif coils["enable"] and coils["auto_mode"]:
        return "MACHINE READY"
    else:
        return "MACHINE NOT READY"

class Plc:
    def __init__(self, ip=PLC_IP, port=PORT):
        self.client = ModbusTcpClient(ip, port=port)
        self.ip = ip
        self.port = port

    def connect(self):
        return self.client.connect()

    def close(self):
        self.client.close()

    def read_coil(self, addy):
        result = self.client.read_coils(addy, count = 1)

        if result.isError():
            raise RuntimeError(result)
        return result.bits[0]

    def read_register(self, addy):
        result = self.client.read_holding_registers(addy, count=2)
        if result.isError():
            raise RuntimeError(result)
        return result.registers[0]

    def read_status(self):
        coils = {}
        for name, address in COILS.items():
            coils[name] = self.read_coil(address)
        parts = self.read_register(PART_COUNT_REGISTER)
        machine_state = get_state(coils)
        return{
            "PARTS ": parts,
            "machine_state": machine_state,
            **coils,
        }
     
