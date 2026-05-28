from time import sleep
import os
import csv
from datetime import datetime

from plc_client import Plc

COILS = {
    "full":16384,
    "robot_moving":16385,
    "photoeye":16386,
    "auto_mode":16387,
    "enable":16388,
        }

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


def on_off(coil):
    if coil:
        return(f"{colors['GREEN']}ON{colors['RESET']}")
    return(f"{colors['RED']}OFF{colors['RESET']}")
def machine_state(state):
    if state == "ROBOT MOVING":
        return f"{colors['CYAN']}{state}{colors['RESET']}"
    elif state == "STOPPED: REQUIRE PICKUP":
        return f"{colors['YELLOW']}{state}{colors['RESET']}"
    elif state == "MACHINE READY":
        return f"{colors['GREEN']}{state}{colors['RESET']}"
    else:
        return f"{colors['RED']}{state}{colors['RESET']}"

def print_status(status):
    os.system("clear")
    print(f"{colors['BOLD']}{colors['GREEN']}Connected to PLC{colors['RESET']}")

    for name in COILS:
        print(f"{name:<18}{on_off(status[name])}")

    print(f"{'PART COUNT':<18}{colors['BLUE']}{status['parts']}{colors['RESET']}")
    print("_"*32)
    print(f"{'MACHINE STATE':<18}{machine_state(status['machine_state'])}{colors['RESET']}")

def write_csv_header(writer):
    writer.writerow([
        "Time stamp",
        "Part Count",
        *COILS.keys(),
        "Machine State",
    ])

def write_csv_row(writer, status):
    writer.writerow([
            datetime.now().isoformat(timespec="seconds"),
            status["parts"],
            *[status[name] for name in COILS],
            status['machine_state'],
    ])


def main():
    plc = Plc()
    if not plc.connect():
        print(f"{colors['RED']}Unable to connect to PLC.")
        sleep(2)
        raise SystemExit

    try:
        os.makedirs("plc_logs", exist_ok=True)
        log_path="plc_logs/plc_data.csv"
        write_header = not os.path.exists(log_path) or os.path.getsize(log_path) == 0
        with open(log_path, "a", newline="") as f:
            writer = csv.writer(f)
            if write_header:
                write_csv_header(writer)

            while True:
                status = plc.read_status()
                print_status(status)
                write_csv_row(writer, status)
                f.flush()
                sleep(.2)
    finally: plc.close()


if __name__ == "__main__":
    main()
