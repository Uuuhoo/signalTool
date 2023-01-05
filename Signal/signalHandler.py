import re

import pyvisa
from Signal.signalCmd import *
# from signalCmd import *
import wx

# 信号发生器地址
usb_addr1 = 'USB0::0x1AB1::0x0642::DG1ZA201902214::INSTR'  # 编号为 GEN_007
usb_addr2 = 'USB0::0x1AB1::0x0642::DG1ZA212302446::INST1R'  # 编号为 AF2014
# 信号发生器相关参数
visa_dll = 'c:/windows/system32/visa32.dll'


class SignalInfo:
    def __init__(self):
        self.signalHWAddrs = []
        self.OpenSignalAddr()
        self.__signalNowAddr = ''

    def OpenSignalAddr(self):
        """打开SignalHadrwareAddr.ini中的信号发生器地址"""
        addr_pattern = re.compile(r'[\[](.*?)[\]]', re.S)
        try:
            with open('./Signal/SignalHadrwareAddr.ini', encoding='utf-8') as file:
                content = file.readlines()
        except FileNotFoundError:
            content = None
            wx.MessageBox("Signal目录下未找到SignalHadrwareAddr.ini配置文件", wx.OK, None)
        if content is not None:
            for line in content:
                try:
                    addr = re.findall(addr_pattern, line)[0]
                except IndexError:
                    wx.MessageBox("SignalHadrwareAddr.ini配置文件中的信号发生器地址格式异常！", wx.OK)
                    return
                self.signalHWAddrs.append(addr)

    def SetNowAddr(self, addr):
        self.__signalNowAddr = addr

    def GetNowAddr(self):
        return self.__signalNowAddr


class SignalTool:
    def __init__(self):
        self.rm = pyvisa.ResourceManager(visa_dll)
        self.signalObject = None
        self.signalCMD = SignalCMD()
        self.signalInfo = SignalInfo()

    def GetConnectStatus(self) -> bool:
        if self.signalObject is not None:
            return True
        else:
            return False

    def DoConnect(self) -> bool:
        """连接信号发生器"""
        signalInfo = SignalInfo()
        for hwAddr in signalInfo.signalHWAddrs:
            try:
                self.signalObject = self.rm.open_resource(hwAddr)  # 遍历所有信号发生器地址
                self.signalInfo.SetNowAddr(hwAddr)
                return True
            except pyvisa.errors.VisaIOError:
                self.signalObject = None
                return False
        del signalInfo

    def SendSignalCmd(self, cmd):
        try:
            self.signalObject.write(cmd)
        except:
            wx.MessageBox("请检查信号发生器连接状态！", "警告", wx.ICON_WARNING)
            print("信号发生器发送命令失败")
            self.signalObject = None
