import re

import pyvisa
import re
import wx

# 信号发生器地址
usb_addr1 = 'USB0::0x1AB1::0x0642::DG1ZA201902214::INSTR'  # 编号为 GEN_007
usb_addr2 = 'USB0::0x1AB1::0x0642::DG1ZA212302446::INST1R'  # 编号为 AF2014
# 信号发生器相关参数
visa_dll = 'c:/windows/system32/visa32.dll'


class cmdType(enumerate):
    VariableParamName = 'VariableParamName'
    Vh = 'VolHigh'
    Vl = 'VolLow'
    Tr = 'TimeRise'
    Td = 'TimeDecline'
    Tp = 'Period'
    Tn = 'CyclingTimes'
    LowHighStep = 'low_high_step'
    JudgeDelay = 'JudgeDelayTime_MS'


class CmdAnalyse:
    def __init__(self, cmd: str):
        self._cmd = cmd
        self._variableParamName = ''
        self._Vh = ''
        self._Vl = ''
        self._Tr = ''
        self._Td = ''
        self._Tp = ''
        self._Tn = ''
        self._low_high_step = []
        self._judge_delay = ''
        self._AnalyseCmd()

    def __del__(self):
        pass

    def _AnalyseCmd(self):
        cmds = self._cmd.split(',')
        Vh = cmds[0]  # 高电平得到的是mV，需要V
        Vl = cmds[1]  # 低电平得到的是mV，需要V
        Tr = cmds[2]  # 上升沿得到的是ns，需要s
        Td = cmds[3]  # 下降沿得到的是ns，需要s
        Tp = cmds[4]  # 周期得到的是ms，需要s
        Tn = cmds[5]  # 次数
        JudgeDelay = cmds[6]
        variablePattern = '\d+\_\d+\_\d+'
        mathPattern = '\d+'
        self._Vh = str(float(re.search(mathPattern, Vh).group()) / 1000)  # 高电平单位mV->V
        self._Vl = str(float(re.search(mathPattern, Vl).group()) / 1000)  # 低电平单位mV->V
        self._Tr = str(float(re.search(mathPattern, Tr).group()) / 1000000000)  # 上升沿单位ns->s
        self._Td = str(float(re.search(mathPattern, Td).group()) / 1000000000)  # 上升沿单位ns->s
        self._Tp = str(float(re.search(mathPattern, Tp).group()) / 1000)  # 周期单位ms->s
        self._Tn = re.search(mathPattern, Tn).group()
        self._JudgeDelay = str(re.search(mathPattern, JudgeDelay).group())  # 判断延时ms
        if re.search(variablePattern, Vh) is not None:
            self._variableParamName = cmdType.Vh
            self._Vh = re.search(variablePattern, Vh).group()
            self._low_high_step = self._Vh.split('_')
            self._low_high_step[0] = str(float(self._low_high_step[0]) / 1000)  # 电平单位mV->V
            self._low_high_step[1] = str(float(self._low_high_step[1]) / 1000)  # 电平单位mV->V
            self._low_high_step[2] = str(float(self._low_high_step[2]) / 1000)  # 电平单位mV->V
        elif re.search(variablePattern, Vl) is not None:
            self._variableParamName = cmdType.Vl
            self._Vl = re.search(variablePattern, Vl).group()
            self._low_high_step = self._Vl.split('_')
            self._low_high_step[0] = str(float(self._low_high_step[0]) / 1000)  # 电平单位mV->V
            self._low_high_step[1] = str(float(self._low_high_step[1]) / 1000)  # 电平单位mV->V
            self._low_high_step[2] = str(float(self._low_high_step[2]) / 1000)  # 电平单位mV->V
        elif re.search(variablePattern, Tr) is not None:
            self._variableParamName = cmdType.Tr
            self._Tr = re.search(variablePattern, Vh).group()
            self._low_high_step = self._Tr.split('_')
            self._low_high_step[0] = str(float(self._low_high_step[0]) / 1000000000)  # 时间单位ns->s
            self._low_high_step[1] = str(float(self._low_high_step[1]) / 1000000000)  # 时间单位ns->s
            self._low_high_step[2] = str(float(self._low_high_step[2]) / 1000000000)  # 时间单位ns->s
        elif re.search(variablePattern, Td) is not None:
            self._variableParamName = cmdType.Td
            self._Td = re.search(variablePattern, Vh).group()
            self._low_high_step = self._Td.split('_')
            self._low_high_step[0] = str(float(self._low_high_step[0]) / 1000000000)  # 时间单位ns->s
            self._low_high_step[1] = str(float(self._low_high_step[1]) / 1000000000)  # 时间单位ns->s
            self._low_high_step[2] = str(float(self._low_high_step[2]) / 1000000000)  # 时间单位ns->s
        else:
            self._variableParamName = ''

    def GetVh(self):
        """获取高电平电压，单位是mv"""
        return self._Vh

    def GetVl(self):
        """获取低电平电压，单位是mv"""
        return self._Vl

    def GetTr(self):
        """获取上升沿时间，单位是ns"""
        return self._Tr

    def GetTd(self):
        """获取下降沿时间，单位是ns"""
        return self._Td

    def GetPeriod(self):
        """获取周期，单位是ms"""
        return self._Tp

    def GetTimes(self):
        """获取循环次数"""
        return self._Tn

    def GetVariableParamName(self):
        """获取可变参数项的名称"""
        return self._variableParamName

    def GetLowHighStepValue(self):
        """获取可变参数的最小值，最大值，步长"""
        return self._low_high_step

    def GetJudgeDelayValue(self):
        """获取校验结果延时参数，ms"""
        return self._JudgeDelay


class SignalInfo:
    def __init__(self):
        self.signalHWAddrs = []
        self.OpenSignalAddr()
        self.__signalNowAddr = ''

    def OpenSignalAddr(self):
        """打开SignalHardwareAddr.ini中的信号发生器地址"""
        addr_pattern = re.compile(r'[\[](.*?)[\]]', re.S)
        try:
            with open('./Signal/SignalHardwareAddr.ini', encoding='utf-8') as file:
                content = file.readlines()
        except FileNotFoundError:
            content = None
            wx.MessageBox("Signal目录下未找到SignalHardwareAddr.ini配置文件", wx.OK, None)
        if content is not None:
            for line in content:
                try:
                    addr = re.findall(addr_pattern, line)[0]
                except IndexError:
                    wx.MessageBox("SignalHardwareAddr.ini配置文件中的信号发生器地址格式异常！", wx.OK)
                    return
                self.signalHWAddrs.append(addr)
        else:
            self.signalHWAddrs.append(usb_addr1)
            self.signalHWAddrs.append(usb_addr2)

    def SetNowAddr(self, addr):
        self.__signalNowAddr = addr

    def GetNowAddr(self):
        return self.__signalNowAddr


class SignalTool:
    def __init__(self):
        self.rm = pyvisa.ResourceManager(visa_dll)
        self.signalObject = None
        self.signalInfo = SignalInfo()

    def GetConnectStatus(self) -> bool:
        """
        获取信号发生器连接状态
        :return: True or False
        """
        # if self.signalObject is not None:
        #     return True
        # else:
        #     return False
        ret = self.SendSignalCmd('*IDN?', True)
        return ret

    def DoConnect(self) -> bool:
        """
        连接信号发生器
        :return: True or False
        """
        signalInfo = SignalInfo()
        ret = False
        for hwAddr in signalInfo.signalHWAddrs:
            try:
                self.signalObject = self.rm.open_resource(hwAddr)  # 遍历所有信号发生器地址
                self.signalInfo.SetNowAddr(hwAddr)
                return True
            except pyvisa.errors.VisaIOError:
                self.signalObject = None
                ret = False
        del signalInfo
        return ret

    def SendSignalCmd(self, cmd, read=False):
        """
        向信号发生器发送控制命令
        :param cmd: cmd
        :param read: 是否读结果,True or False
        :return: None
        """
        try:
            self.signalObject.write(cmd)
            if read:
                ret = self.signalObject.read()
                return ret
            return True
        except:
            wx.MessageBox("请检查信号发生器连接状态！", "警告", wx.ICON_WARNING)
            print("信号发生器发送命令失败")
            self.signalObject = None
            # return False
            raise ConnectionError("信号发生器连接失败！")

    @staticmethod
    def GetOUTPUTCmd(num: int, status: bool) -> str:
        """
        设置信号发生器输出命令
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
        设置信号发生器Beep命令
        :return: 输出cmd
        """
        cmd = ':SYSTem:BEEPer:IMMediate'
        return cmd

    @staticmethod
    def GetAPPLPulsCmd(num: int, freq: str, amp: str, offset: str, phase: str = '0') -> str:
        """
        设置指定通道的波形为具有指定频率、幅度、偏移和相位的脉冲
        :param num:通道1or2
        :param freq:频率=1/周期
        :param amp:幅度=高电平-低电平
        :param offset:偏移=(高电平+低电平)/2
        :param phase:相位，默认为0
        :return:输出cmd
        """
        cmd = ':SOUR%s:APPL:PULS %s,%s,%s,%s' % (str(num), freq, amp, offset, phase)
        return cmd

    @staticmethod
    def GetTRiseCmd(num: int, sec: str) -> str:
        """
        设置指定通道的脉冲上升沿时间
        :param num:通道1or2
        :param sec:时间，单位为秒
        :return:输出cmd
        """
        cmd = ':SOUR%s:FUNC:PULS:TRAN:LEAD %s' % (str(num), sec)
        return cmd

    @staticmethod
    def GetTDeclineCmd(num: int, sec: str) -> str:
        """
        设置指定通道的脉冲下降沿时间
        :param num:通道1or2
        :param sec:时间，单位为秒
        :return:输出cmd
        """
        cmd = ':SOUR%s:FUNC:PULS:TRAN:TRA %s' % (str(num), sec)
        return cmd

    @staticmethod
    def GetDCYCCmd(num: int, per: str = '50') -> str:
        """
        设置指定通道的脉冲占空比
        :param num:通道1or2
        :param per:占空比百分比
        :return: 输出cmd
        """
        cmd = ':SOUR%s:PULS:DCYC %s' % (str(num), per)
        return cmd

    @staticmethod
    def GetFREQCmd(num: int, freq: str) -> str:
        """
        设置信号发生器频率命令
        :param num:通道1or2
        :param freq:频率
        :return: 输出cmd
        """
        cmd = ':SOUR%s:FREQ %s' % (str(num), freq)
        return cmd

    @staticmethod
    def GetVOLTHighCmd(num: int, volH: str) -> str:
        """
        设置指定通道的波形（基本波形和任意波形）高电平值。
        :param num:通道1or2
        :param volH:高电平值，单位为V
        :return: 输出cmd
        """
        cmd = ':SOUR%s:VOLT:HIGH %s' % (str(num), volH)
        return cmd

    @staticmethod
    def GetVOLTLowCmd(num: int, volL: str) -> str:
        """
        设置指定通道的波形（基本波形和任意波形）低电平值。
        :param num:通道1or2
        :param volL:低电平值，单位为V
        :return: 输出cmd
        """
        cmd = ':SOUR%s:VOLT:LOW %s' % (str(num), volL)
        return cmd

    @staticmethod
    def GetPULSPerCmd(num: int, period: str) -> str:
        """
        设置指定通道的脉冲周期。
        :param num:通道1or2
        :param period:周期，单位为秒
        :return: 输出cmd
        """
        cmd = ':SOUR%s:FUNC:PULS:PER %s' % (str(num), period)
        return cmd

    @staticmethod
    def GetPHASCmd(num: int, phase: str) -> str:
        """
        设置指定通道的波形（基本波形和任意波形）起始相位。
        :param num:通道1or2
        :param phase:相位，单位为°
        :return: 输出cmd
        """
        cmd = ':SOUR%s:PHAS %s' % (str(num), phase)
        return cmd

    @staticmethod
    def GetFUNCCmd(num: int, sourceType: str) -> str:
        """
        设置指定通道的波形。
        :param num:通道1or2
        :param sourceType:波形 脉冲：PULS
        :return: 输出cmd
        """
        cmd = ':SOUR%s:FUNC %s' % (str(num), sourceType)
        return cmd
