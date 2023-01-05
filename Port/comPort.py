import serial
import serial.tools.list_ports_windows as serialTools


class ComPort:
    def __init__(self):
        self.comPorts = {}
        self.serialHandler = serial.Serial()
        self.InitComPort()

    def InitComPort(self):
        self.comPorts.clear()
        coms = sorted(serialTools.comports())
        for n, (name, desc, hwid) in enumerate(coms):
            self.comPorts[desc] = name

    def SendData(self, data):
        """send data to com"""
        try:
            self.serialHandler.write(data)
        except:
            return False
        return True



