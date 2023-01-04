import serial
import serial.tools.list_ports_windows as serialTools


class ComPort:
    def __init__(self):
        self.comPorts = []
        self.serialHandler = serial.Serial()
        self.InitComPort()

    def InitComPort(self):
        self.comPorts.clear()
        coms = sorted(serialTools.comports())
        idx = 0
        for n, (name, desc, hwid) in enumerate(coms):
            self.comPorts.append(desc)
