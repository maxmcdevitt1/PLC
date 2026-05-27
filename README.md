# PLC
My PLC scripts in python
| PLC point | What to connect           | What it represents      |

| --------- | ------------------------- | ----------------------- |

**\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_**

| X1        | SPDT toggle switch        | Start / enable          |

| X2        | BEN5M photoeye black wire | Part present sensor     |

| X3        | SPDT toggle switch        | Reset                   |

| X4        | SPDT toggle switch        | Auto mode               |

<b>~~\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_~~</b>

| Y1        | 24 V light                | Cell ready              |

| Y2        | 24 V light                | Conveyor/feed active    |

| Y3        | 24 V light                | Robot request           |

| Y4        | 24 V light                | Robot busy/moving       |

**\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_**



##### **To Add!**

* Fault report generator



###### Information:

* Raspberry Pi is the Modbus TCP client and the CLICK PLC the Modbus TCP server.
* SERVER 192.168.10.30
* PLC IP = 192.168.10.10
* Pi eth0:  192.168.10.20



\[Debian Laptop]

&#x20;    |

&#x20;    | SSH

&#x20;    |

\[Ethernet / WiFi Network]

&#x20;    |

&#x20;    | SSH terminal

&#x20;    |

\[Raspberry Pi]

&#x20;    |

&#x20;    | Modbus TCP, Port 502

&#x20;    |

\[CLICK PLC: 192.168.10.10]

&#x20;    |

&#x20;    | 24VDC inputs / outputs

&#x20;    |

\[Photoeye]   \[Switches]   \[LED Indicators]



###### Debian Laptop:

Remote engineering workstation.

Used to SSH into Raspberry Pi.



###### Raspberry Pi:

Runs Python Modbus client.

Reads PLC coils/registers.

Displays part count, photoeye state, robot request, and busy state.



###### CLICK PLC:

Controls machine logic.

Handles photoeye, timer, counter, robot request, busy simulation, and reset.



###### Photoeye:

Detects parts.



###### LEDs:

Show part detected, robot request, and busy status.



| Device                       |          PLC Address | Type            | Purpose                        |
| ---------------------------- | -------------------: | --------------- | ------------------------------ |
| SPDT 1 Enable                |                 X001 | Input           | Enables system                 |
| Photoeye                     |                 X002 | Input           | Detects part                   |
| SPDT 2 Robot Request / Reset |                 X003 | Input           | Starts robot/busy simulation   |
| SPDT 3 Auto                  |                 X004 | Input           | Auto mode                      |
| LED 2 Part Detected          |                 Y002 | Output          | Shows photoeye detection       |
| LED 3 Robot Request          |                 Y003 | Output          | Batch complete / robot request |
| LED 4 Busy                   |                 Y004 | Output          | Robot busy simulation          |
| C1                           |          Modbus coil | Internal        | Pi reads robot request         |
| C2                           |          Modbus coil | Internal        | Pi reads busy                  |
| C3                           |          Modbus coil | Internal        | Pi reads photoeye              |
| CTD1                         | Modbus register/data | Counter current | Pi reads part count            |


24VDC Power Supply
+24V  ───────────────┬───────────── SPDT 1 ───── PLC X001
                     ├───────────── Photoeye ─── PLC X002
                     ├───────────── SPDT 2 ───── PLC X003
                     └───────────── SPDT 3 ───── PLC X004

0V    ───────────────┬───────────── PLC input common
                     └───────────── Sensor 0V / return
PLC Y001 ───────── LED 1 Cell Ready  ───────── Output common / 0V
PLC Y002 ───────── LED 2 Part Detected ───────── Output common / 0V
PLC Y003 ───────── LED 3 Robot Request ───────── Output common / 0V
PLC Y004 ───────── LED 4 Busy ────────────────── Output common / 0V
