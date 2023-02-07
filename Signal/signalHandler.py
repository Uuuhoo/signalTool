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
        """
        获取信号发生器连接状态
        :return: True or False
        """
        if self.signalObject is not None:
            return True
        else:
            return False

    def DoConnect(self) -> bool:
        """
        连接信号发生器
        :return: True or False
        """
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

    def SendSignalCmd(self, cmd) -> None:
        """
        向信号发生器发送控制命令
        :param cmd: cmd
        :return: None
        """
        try:
            self.signalObject.write(cmd)
        except:
            wx.MessageBox("请检查信号发生器连接状态！", "警告", wx.ICON_WARNING)
            print("信号发生器发送命令失败")
            self.signalObject = None

    @staticmethod
    def GetOUTPUTCmd(num: int, status: bool) -> str:
        """
        获取信号发生器输出命令
        :param status: True: ON , False: OFF
        :param num: 通道1or2
        :return: 输出cmd
        """
        if status:
            temp = 'ON'
        else:
            temp = 'OFF'
        cmd = ':OUTPUT%s %s' % (str(num), temp)
        return cmd

    @staticmethod
    def GetBEEPCmd() -> str:
        """
        获取信号发生器Beep命令
        :return: 输出cmd
        """
        cmd = ':SYSTem:BEEPer:IMMediate'
        return cmd

    @staticmethod
    def GetAPPLPULSCmd(num: int, freq: str, amp: str, offset: str, phase: str = '0') -> str:
        """
        设置指定通道的波形为具有指定频率、幅度、偏移和相位的脉冲
        :param num:通道1or2
        :param freq:频率
        :param amp:幅度
        :param offset:偏移
        :param phase:相位，默认为0
        :return:输出cmd
        """
        cmd = ':SOUR%s:APPL:PULS %s,%s,%s,%s' % (str(num), freq, amp, offset, phase)
        return cmd

    @staticmethod
    def GetTRISECMD(num:int, sec:str) -> str:
        """
        设置指定通道的脉冲上升沿时间
        :param num:通道1or2
        :param sec:时间以秒为单位
        :return:输出cmd
        """
        cmd = ':SOUR%s:FUNC:PULS:TRAN:LEAD %s'% (str(num), sec)
        return cmd

    @staticmethod
    def GetTDOWNCMD(num:int, sec:str) -> str:
        """
        设置指定通道的脉冲下降沿时间
        :param num:通道1or2
        :param sec:时间以秒为单位
        :return:输出cmd
        """
        cmd = ':SOUR%s:FUNC:PULS:TRAN:TRA %s'% (str(num), sec)
        return cmd

    @staticmethod
    def GetDCYCCMD(num:int, per:str = '50') -> str:
        """
        设置指定通道的脉冲占空比
        :param num:通道1or2
        :param per:占空比百分比
        :return: 输出cmd
        """
        cmd = ':SOUR%s:PULS:DCYC %s' % (str(num), per)
        return cmd

    @staticmethod
    def GetBEEPCmd() -> str:
        """
        获取信号发生器Beep命令
        :return: 输出cmd
        """
        cmd = ':SYSTem:BEEPer:IMMediate'
        return cmd
