import pyvisa
from Signal.signalCmd import *
# from signalCmd import *
import wx


# 信号发生器地址
usb_addr1 = 'USB0::0x1AB1::0x0642::DG1ZA201902214::INSTR'  # 编号为 GEN_007
usb_addr2 = 'USB0::0x1AB1::0x0642::DG1ZA212302446::INST1R'  # 编号为 AF2014
# 信号发生器相关参数
visa_dll = 'c:/windows/system32/visa32.dll'


class SignalCMD:
    Beep = ':SYSTem: BEEPer:IMMediate'
    Output1On = ':OUTPUT1 ON'
    Output1Off = ':OUTPUT1 OFF'


class SignalInfo:
    def __init__(self):
        self.signalHWAddrs = []
        self.signalHWAddrs.append(usb_addr1)
        self.signalHWAddrs.append(usb_addr2)
        try:
            with open('./Signal/SignalHadrwareAddr.ini', encoding='utf-8') as file:
                content = file.read()
        except FileNotFoundError:
            content = None
        if content is not None:
            for line in content.split('\n'):
                addr = line.split('[')[1][:-1]


class SignalTool:
    def __init__(self):
        self.rm = pyvisa.ResourceManager(visa_dll)
        self.signalObject = None
        self.signalCMD = SignalCMD()
        self.signalInfo = SignalInfo()

    def getIsConnected(self):
        if self.signalObject is not None:
            return True
        else:
            return False

    def toConnect(self):
        """连接信号发生器"""
        signalInfo = SignalInfo()
        for hwAddr in signalInfo.signalHWAddrs:
            try:
                self.signalObject = self.rm.open_resource(hwAddr)  # 遍历所有信号发生器地址
                return True
            except:
                self.signalObject = None
        if self.signalObject is None:
            return False

    def sendSignalCmd(self, cmd):
        try:
            self.signalObject.write(cmd)
        except:
            wx.MessageBox("请检查信号发生器连接状态！", "警告", wx.ICON_WARNING)
            print("信号发生器发送命令失败")
            self.signalObject = None
