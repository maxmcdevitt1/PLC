import time
import os
from pymodbus.client import ModbusTcpClient
import csv
from datetime import datetime

PLC_IP = "192.168.10.10"
PORT = 502

def get_state(coils):
    if coils["ROBOT MOVING"]:
        return "ROBOT MOVING"
    elif coils["FULL"]:
        return "STOPPED: REQUIRE PICKUP"
    elif coils["ENABLE"] and coils["AUTO MODE"]:
        return "MACHINE READY"
    else:
        return "MACHINE NOT READY"

c_addresses = {
    "FULL" : 16384,         # Y3
    "ROBOT MOVING" : 16385,          # Y4
    "PHOTOEYE" : 16386,      # X2
    "AUTO MODE" : 16387,     # X4 X1
    "ENABLE" : 16388         # X1
}
register_addresses = 49152
colors = {
    # Terminal colors
    "RESET":"\033[0m",
    "BOLD":"\033[1m",
    "GREEN":"\033[92m",
    "RED":"\033[91m",
    "YELLOW":"\033[93m",
    "BLUE":"\033[94m",
    "CYAN":"\033[96m",
    "GRAY":"\033[90m",
}

def clear_screen():
    os.system("clear")

class Plc:
    def __init__(self, ip, port):
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

def on_off(coil):
    if coil:
        return(f"{colors['GREEN']}ON{colors['RESET']}")
    return(f"{colors['RED']}OFF{colors['RESET']}")

client = Plc(PLC_IP, PORT)
if not client.connect():
    print(f"{colors['RED']}Unable to connect to PLC.")
    time.sleep(2)
    raise SystemExit

try:
        os.makedirs("plc_logs", exist_ok=True)
        with open("plc_logs/plc_data.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
            "timestamp",
            "part_count",
            *c_addresses.keys(),
            "machine_state"
            ])

            coils = {}
            while True:

                os.system("clear")
                parts = client.read_register(register_addresses)
                print(f"{colors['BOLD']}{colors['GREEN']}Connected to PLC{colors['RESET']}")

                for name, address in c_addresses.items():
                    result = client.read_coil(address)
                    coils[name]=result
                
                for name, result in coils.items():
                    print(f"{name:<16}{on_off(result)}")
                state = get_state(coils=coils)

                writer.writerow([
                    datetime.now().isoformat(timespec="seconds"),
                    parts,
                    *coils.values(),
                    state,
                ])
                file.flush()
                
                print(f"{"Part Count":<16}{colors['BLUE']}{parts}{colors['RESET']}")
                print("_"*28)
                
                if coils["ROBOT MOVING"]:
                    print(f"{'MACHINE STATE':<16}{colors['BLUE']}ROBOT IS MOVING")
                elif coils["FULL"]:
                    print(f"{'MACHINE STATE':<16}{colors['YELLOW']}STOPPED: REQUIRE PICKUP")
                elif coils["ENABLE"] and coils["AUTO MODE"]:
                    print(f"{'MACHINE STATE':<16}{colors['GREEN']}ROBOT READY")
                else:
                    print(f"{'MACHINE STATE':<16}{colors['RED']}NOT READY")
                
                time.sleep(.2)


finally:
    client.close()