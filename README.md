# PLC Conveyor Cell Simulator

A bench-top, DIN-rail-mounted PLC training cell that simulates a conveyor-to-robot transfer station. A real photoelectric sensor detects parts, toggle switches simulate operator inputs, pilot lights show machine status, and a Raspberry Pi polls the PLC over Modbus TCP and serves a web-based HMI.

## Hardware

- **PLC:** AutomationDirect CLICK C0-10DD1E-D (24 VDC, sinking outputs, Ethernet, Modbus TCP)
- **Sensor:** Taiss BEN5M photoelectric sensor
- **I/O:** SPDT toggle switches, 24 VDC pilot lights
- **Power:** 24 VDC supply
- **Compute:** Raspberry Pi 4 (Modbus TCP client + Flask HMI server)

## Network

| Device         | IP             | Role                  |
| -------------- | -------------- | --------------------- |
| CLICK PLC      | 192.168.10.10  | Modbus TCP server     |
| Raspberry Pi   | 192.168.10.20  | Modbus client + HMI   |
|  PC | *  | SSH workstation       |

```
[Laptop] --SSH--> [Raspberry Pi] --Modbus TCP/502--> [CLICK PLC] --24V I/O--> [Photoeye / Switches / LEDs]
```

## I/O Map

| PLC Address | Device                | Purpose                  |
| ----------- | --------------------- | ------------------------ |
| X001        | SPDT 1                | Enable                   |
| X002        | BEN5M photoeye        | Part detect              |
| X003        | SPDT 2                | Robot request / reset    |
| X004        | SPDT 3                | Auto mode                |
| Y001        | LED                   | Cell ready               |
| Y002        | LED                   | Part detected            |
| Y003        | LED                   | Robot request            |
| Y004        | LED                   | Robot busy               |
| C1-C5| Modbus coils          | Request / busy / photoeye |
| CTD1        | Modbus register       | Part count               |

## Software

- `src/plc_client.py` &mdash; Modbus TCP client (reads coils + part count register)
- `src/HMI.py` &mdash; Flask server, polls the PLC in a background thread and exposes `/api/status`
- `src/templates/index.html` &mdash; industrial-style HMI dashboard (auto-refreshes once per second)
- `src/plcstatus.py` &mdash; status helper

## Run

```bash
pip install flask pymodbus
python src/HMI.py
```

Then browse to `http://<pi-ip>:5000`.

## To Do

- Fault report generator
