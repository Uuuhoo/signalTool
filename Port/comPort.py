import serial
import serial.tools.list_ports_windows as serialTools
import wx


class ComPort:
    def __init__(self):
        self.__comPorts = {}
        self.serialHandler = serial.Serial()
        self.InitComPort()

    def GetFlushComPorts(self):
        self.InitComPort()
        return self.__comPorts

    def InitComPort(self):
        self.__comPorts.clear()
        coms = sorted(serialTools.comports())
        for n, (name, desc, hwid) in enumerate(coms):
            self.__comPorts[desc] = name

    def SendData(self, data):
        """send data to com"""
        try:
            self.serialHandler.write(data)
        except:
            return False
        return True

    def ReceiveData(self):
        recvData = self.serialHandler.read()
        while self.serialHandler.inWaiting() > 0 and self.serialHandler.isOpen():
            recvData += self.serialHandler.read(self.serialHandler.inWaiting())
            wx.MilliSleep(10)
        return recvData



