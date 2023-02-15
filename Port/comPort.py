import serial
import serial.tools.list_ports_windows as serialTools
import wx
import wx.lib.newevent

(PostDataEvent, EVT_DATA) = wx.lib.newevent.NewEvent()  # 发送数据至其他线程


class ComPort:
    def __init__(self):
        self.__comPorts = {}
        self.serialHandler = serial.Serial()
        self.doReceive = False
        self.InitComPort()

    def GetFlushComPorts(self):
        self.InitComPort()
        return self.__comPorts

    def GetSerialHandler(self):
        """return serial handler"""
        return self.serialHandler

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

    def ReceiveData(self, win, stop_threads):
        """Receive Data from com"""
        recvData = ''
        self.doReceive = True
        if self.GetSerialHandler().isOpen():
            self.serialHandler.reset_input_buffer()

        while not stop_threads():
            try:
                recvData = self.serialHandler.read()
            except:
                wx.MilliSleep(10)

            while self.serialHandler.inWaiting() > 0 and self.serialHandler.isOpen():
                recvData += self.serialHandler.read(self.serialHandler.inWaiting())
                wx.MilliSleep(10)
                if stop_threads():
                    return

            if len(recvData):
                evt = PostDataEvent(value=recvData.hex().upper())
                wx.PostEvent(win, evt)

        return
