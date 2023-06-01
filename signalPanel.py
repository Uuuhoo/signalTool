import os
import queue
import time

import serial
import wx
import copy
import Port.comPort as ComPort
import Signal.signalHandler as SignalHandler
import Gui.guiSignal as GuiSignal
import threading
import sched
from datetime import datetime
from decimal import Decimal

global global_interval


class SignalToolMainPanel(GuiSignal.signalToolMainPanel):
    def __init__(self, parent):
        GuiSignal.signalToolMainPanel.__init__(self, parent)
        self.mainFrame = parent
        self.row = 0
        self.comPort = ComPort.ComPort()
        self.runHandle = None  # 主线程
        self.recvHandle = None  # 接收线程
        self.judgeHandle = None  # 判断线程
        self.condition = threading.Condition()
        self.dataQueue = queue.Queue()
        self.stop_threads = False  # 停止线程标识
        self.schedule = sched.scheduler(time.time, time.sleep)
        self.Bind(ComPort.EVT_DATA, self.ReceiveProcess)
        self.signalHandler = SignalHandler.SignalTool()
        self.PortInit()

        self.err_cnt = 0

    def Close(self, force=False):
        self.Destroy()

    def Destroy(self):
        wx.CallAfter(self.StopThread)

    def PortInit(self):
        """
        刷新端口列表并显示
        :return:
        """
        wx.CallAfter(self.m_ccMiddlePort.SetItems, list(self.comPort.GetFlushComPorts().keys()))
        wx.CallAfter(self.m_ccMiddlePort.SetSelection, 0)

    def OnButtonSignalConnectClick(self, event) -> None:
        """连接信号发生器"""
        self.ConnectSignal()
        event.Skip()

    def ConnectSignal(self):
        if not self.signalHandler.DoConnect():
            wx.MessageBox("信号发生器连接失败，请检查连接状态！", "Warning!")
            wx.CallAfter(self.m_textSignalAddr.SetValue, "")
            wx.CallAfter(self.m_btnSignalConnect.SetLabelText, "连接信号发生器")
            print('信号发生器连接失败！')
            return
        self.signalHandler.SendSignalCmd(self.signalHandler.GetBEEPCmd())
        wx.CallAfter(self.m_textSignalAddr.SetValue, self.signalHandler.signalInfo.GetNowAddr())
        wx.CallAfter(self.m_btnSignalConnect.SetLabelText, "已连接信号发生器")

    def OnButtonMiddleConnectClick(self, event):
        """连接主控点击事件"""
        wx.CallAfter(self.ConnectMainControl)
        event.Skip()

    def ConnectMainControl(self):
        """连接主控"""
        port = self.comPort.GetFlushComPorts().get(self.m_ccMiddlePort.GetStringSelection())
        baud = int(self.m_ccMiddleBaud.GetStringSelection())
        bitsize = self.m_ccMiddleDBitNum.GetStringSelection()
        check = self.m_ccMiddleCheck.GetStringSelection()
        check = 'None'  # 固定不校验
        stopsize = self.m_ccMiddleStopBit.GetStringSelection()

        Parity = {'None': 'N', 'Even': 'E', 'Odd': 'O'}
        DataBits = {'5': 5, '6': 6, '7': 7, '8': 8}
        StopBits = {'1': 1, '1.5': 1.5, '2': 2}
        self.comPort.serialHandler.close()
        # wx.MilliSleep(50)

        self.comPort.serialHandler.port = port
        self.comPort.serialHandler.baudrate = baud
        self.comPort.serialHandler.parity = Parity[check]
        self.comPort.serialHandler.bytesize = DataBits[bitsize]
        self.comPort.serialHandler.stopbits = StopBits[stopsize]
        # self.comPort.timeout = 0.5

        if self.m_btn_MiddleConnect.GetLabel() == "连接主控":
            try:
                self.comPort.serialHandler.open()
                # wx.MilliSleep(50)
            except serial.SerialException:
                wx.MessageBox("打开 " + str(self.comPort.serialHandler.port) + "失败！", "警告！", wx.OK)
                return
            wx.CallAfter(self.m_btn_MiddleConnect.SetLabelText, "断开主控")
        elif self.m_btn_MiddleConnect.GetLabel() == "断开主控":
            self.comPort.serialHandler.close()
            wx.CallAfter(self.m_btn_MiddleConnect.SetLabelText, "连接主控")

    def OnButtonMiddleFlushClick(self, event):
        """刷新主控接口"""
        wx.CallAfter(self.PortInit)

    def OnButtonClearTestResultClick(self, event):
        """清空测试结果"""
        wx.CallAfter(self.m_resultGrid.ClearGrid)
        self.row = 0
        event.Skip()

    def OnButtonStartTestClick(self, event):
        """开始测试按钮"""
        if len(self.m_listTestCase.GetStrings()) == 0:
            wx.MessageBox('无测试项！', '警告')
            return

        if self.comPort.GetSerialHandler().isOpen() is False:
            wx.MessageBox('串口未打开，将只操控信号发生器！', '警告')

        self.stop_threads = False
        if self.runHandle is None:
            self.runHandle = threading.Thread(target=self.startTest, args=(lambda: self.stop_threads,))
            if self.runHandle.is_alive() is False:
                self.runHandle.setName('信号发生器开始测试线程')
                self.runHandle.start()
        else:
            wx.MessageBox('测试正在进行中！', '警告')

        if self.comPort.GetSerialHandler().isOpen() is not False:
            if self.recvHandle is None:
                self.recvHandle = threading.Thread(target=self.comPort.ReceiveData,
                                                   args=(self, lambda: self.stop_threads,))
                if self.recvHandle.is_alive() is False:
                    self.recvHandle.start()
        event.Skip()

    def startTest(self, stop_threads):
        """
        开始测试函数
        :param stop_threads:线程停止标识
        :return:None
        """
        # self.ConnectSignal()
        self.stop_threads = False
        cmdType = SignalHandler.cmdType
        testQueue = []
        testCase = self.m_listTestCase.GetStrings()
        # 解析信号发生器控制命令
        for case in testCase:
            cmdAnalysed = SignalHandler.CmdAnalyse(case)
            tempItem = ({cmdType.VariableParamName: cmdAnalysed.GetVariableParamName(),
                         cmdType.Vh: cmdAnalysed.GetVh(),
                         cmdType.Vl: cmdAnalysed.GetVl(),
                         cmdType.Tr: cmdAnalysed.GetTr(),
                         cmdType.Td: cmdAnalysed.GetTd(),
                         cmdType.Tp: cmdAnalysed.GetPeriod(),
                         cmdType.Tn: cmdAnalysed.GetTimes(),
                         cmdType.LowHighStep: cmdAnalysed.GetLowHighStepValue(),
                         cmdType.JudgeDelay: cmdAnalysed.GetJudgeDelayValue()
                         })
            testQueue.append(copy.deepcopy(tempItem))
        try:
            self.signalHandler.SendSignalCmd(self.signalHandler.GetOUTPUTCmd(1, False))  # 关闭通道1
        except ConnectionError:
            self.ConnectError(0)
            return False
        # 根据解析完的命令依次进行测试
        for i in range(len(testQueue)):
            if stop_threads():
                wx.CallAfter(self.m_gaugeProcess.SetValue, 0)
                return
            nowTest = testQueue[i]
            if nowTest.get(cmdType.VariableParamName) == cmdType.Vh:
                pass
            elif nowTest.get(cmdType.VariableParamName) == cmdType.Vl:
                lvs = nowTest.get(cmdType.LowHighStep)
                low = Decimal(lvs[0])
                high = Decimal(lvs[1])
                step = Decimal(lvs[2])
                self.m_gaugeProcess.SetLabelText('kaishiceshi')
                wx.CallAfter(self.m_gaugeProcess.SetRange, len(testQueue)*((high-low)/step+1))
                nowQueue = i+1
                nowProcessValue = 0
                wx.CallAfter(self.m_btnStartTest.Disable)
                wx.CallAfter(self.m_btnStartTest.SetLabelText, str(nowQueue)+'/'+str(len(testQueue)))
                _err_flag = False
                ret = []
                try:
                    self.signalHandler.SendSignalCmd(self.signalHandler.GetFUNCCmd(1, 'PULS'))  # 设置波形为脉冲
                    self.signalHandler.SendSignalCmd(self.signalHandler.GetPULSPerCmd(1, nowTest.get(cmdType.Tp)))  # 周期
                    self.signalHandler.SendSignalCmd(self.signalHandler.GetVOLTHighCmd(1, nowTest.get(cmdType.Vh)))  # 高电平
                    self.signalHandler.SendSignalCmd(self.signalHandler.GetVOLTLowCmd(1, str(low)))  # 低电平
                    self.signalHandler.SendSignalCmd(self.signalHandler.GetTRiseCmd(1, nowTest.get(cmdType.Tr)))  # 上升沿
                    self.signalHandler.SendSignalCmd(self.signalHandler.GetTDeclineCmd(1, nowTest.get(cmdType.Td)))  # 下降沿
                    self.signalHandler.SendSignalCmd(self.signalHandler.GetDCYCCmd(1, '50'))  # 占空比
                    self.signalHandler.SendSignalCmd(self.signalHandler.GetPHASCmd(1, '180'))  # 相位
                    self.signalHandler.SendSignalCmd(self.signalHandler.GetOUTPUTCmd(1, True))  # 开启通道1
                except ConnectionError:
                    self.ConnectError(0)
                    return False
                while low <= high and not stop_threads():

                    try:
                        self.OnceCyclingStart()
                        self.signalHandler.SendSignalCmd(self.signalHandler.GetVOLTLowCmd(1, str(low)))  # 低电平
                        self.signalHandler.SendSignalCmd(self.signalHandler.GetOUTPUTCmd(1, True))  # 开启通道1
                    except ConnectionError:
                        self.ConnectError(0)
                        return False
                    print('-------start time2:' + str(time.time()))
                    global global_interval
                    global_interval = (time.time() - global_interval) * 1000
                    print('--------interval is :'+str(global_interval))
                    # 信号发生器关闭打开实际波形偏移比代码耗时多大概20ms，相位180°，延迟半个周期判断
                    _offset = 0.02 + float(nowTest.get(cmdType.Tp))/2
                    Judge_delay = float(nowTest.get(cmdType.JudgeDelay)) / 1000 + _offset
                    self.err_cnt = 0
                    # 第一个周期上升沿不对，不判断
                    self.JudgeThread(Judge_delay, stop_threads)
                    # 循环次数并判断
                    for _ in range(int(nowTest.get(cmdType.Tn)) - 1):
                        if stop_threads():
                            wx.CallAfter(self.m_gaugeProcess.SetValue, 0)
                            break
                        if self.recvHandle is not None:
                            pass
                        self.schedule.enter(float(nowTest.get(cmdType.Tp)), 1, self.JudgeThread, (Judge_delay,
                                                                                                  stop_threads,))
                        self.schedule.run()

                    if not stop_threads():
                        try:
                            self.schedule.enter(float(nowTest.get(cmdType.Tp)), 1, self.OnceCyclingFinished)
                            self.schedule.run()
                        except ConnectionError:
                            self.ConnectError(0)
                            return False

                    if (self.err_cnt == 0 or low == high) and _err_flag is True:
                        if low == high:
                            err_now = str(int(low * 1000)) + 'mv'
                        else:
                            err_now = str(int((low - step) * 1000)) + 'mv'
                        self.SetRowValue([err_Tr, err_Td, err_low, err_now])
                        self.row += 1
                        _err_flag = False
                        self.err_cnt = 0

                    if self.err_cnt > 0 and _err_flag is False:
                        _err_flag = True
                        err_Tr = str(int(float(nowTest.get(cmdType.Tr)) * 1000000000)) + 'ns'
                        err_Td = str(int(float(nowTest.get(cmdType.Td)) * 1000000000)) + 'ns'
                        err_low = str(int(low * 1000)) + 'mv'
                        print('error in ' + err_low + ' with Tr: ' + err_Tr
                              + ' and Td: ' + err_Td)
                        self.SetRowValue([err_Tr, err_Td, err_low])

                    print('-------finished time:' + str(time.time()))
                    low += step
                    nowProcessValue += 1
                    wx.CallAfter(self.m_gaugeProcess.SetValue,
                                 self.m_gaugeProcess.GetRange() / len(testQueue) * (nowQueue - 1) + nowProcessValue)

            elif nowTest.get(cmdType.VariableParamName) == cmdType.Tr:
                pass
            elif nowTest.get(cmdType.VariableParamName) == cmdType.Td:
                pass
            elif nowTest.get(cmdType.VariableParamName) == '':  # 单点测试
                pass
            else:
                pass
        self.ExitTestThread()
        # self.StopThread()

    def JudgeThread(self, delay: float, stop_threads):
        if self.judgeHandle is None:
            self.judgeHandle = threading.Timer(delay, self.JudgeResult, args=(stop_threads,))
            if self.judgeHandle.is_alive() is False:
                self.judgeHandle.setName('检查结果线程')
                self.judgeHandle.start()

    def JudgeResult(self, stop_threads):

        # self.signalHandler.SendSignalCmd(self.signalHandler.GetOUTPUTCmd(1, False))

        print('run task time:' + str(time.time()))
        self.dataQueue.queue.clear()

        if self.SendProcess('5A') is False:
            self.err_cnt += 1
            self.StopJudgeThread()
            return False
        # wx.MilliSleep(20)
        # recv_data = ''
        self.condition.acquire()
        cnt = 0
        while not stop_threads() and cnt < 4:
            self.condition.wait(0.1)
            recv_data = self.dataQueue.get()
            print('recv ---------:' + recv_data)
            if self.CheckRecvFrame(recv_data) is not True:
                self.err_cnt += 1
                break
            if self.CheckRecvFrame(recv_data) is True:
                break
            if self.CheckRecvFrame(recv_data) is None:
                pass
            cnt += 1
        self.condition.release()
        self.StopJudgeThread()

    @staticmethod
    def CheckRecvFrame(frame: str):
        """
        校验接收命令帧
        :param frame: 接收到的命令
        :return: bool or None
        """
        if len(frame) < 2:
            return None
        if frame == 'A5':
            return True
        else:
            return False

    def OnceCyclingFinished(self):
        """
        指定次数的循环结束后，对芯片进行断电以进行下一个测试条件
        :return: None
        """
        try:
            self.signalHandler.SendSignalCmd(self.signalHandler.GetOUTPUTCmd(1, False))  # 关闭通道1
        except ConnectionError:
            raise ConnectionError("信号发生器连接失败！")
        print('-------close signal time:' + str(time.time()))

    @staticmethod
    def OnceCyclingStart():
        """
        切换低电平时对信号发生器进行初始化操作，不断电
        :return: None or raise Error
        """
        wx.MilliSleep(10)
        print('-------start time1:' + str(time.time()))
        global global_interval
        global_interval = time.time()

    def SendProcess(self, cmd):
        data = bytearray.fromhex(cmd)
        if self.comPort.SendData(data) is False:
            return False
        return True

    def SaveTestResult(self):
        """
        保存测试结果
        :return:None
        """
        headers, cell_values = [], []
        for i in range(self.m_resultGrid.GetNumberCols()):
            headers.append(self.m_resultGrid.GetColLabelValue(i)+' ')
        headers[-1] = headers[-1] + '\n'

        number_row = self.m_resultGrid.GetNumberRows()
        number_col = self.m_resultGrid.GetNumberCols()

        for i in range(number_row):
            temp = []
            for j in range(number_col):
                temp.append(self.m_resultGrid.GetCellValue(i, j)+' ')
            temp[-1] = temp[-1] + '\n'
            cell_values.append(temp)

        nowtime = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
        filepath = '.\\log'
        try:
            with open('.\\log\\' + nowtime + '错误结果.txt', 'w', encoding='utf-8', newline='') as f:
                f.writelines(headers)
                for errInfo in cell_values:
                    f.writelines(errInfo)
                print("异常结果保存成功！")
        except FileNotFoundError:
            os.mkdir(filepath)
            self.SaveTestResult()
            wx.MessageBox("未找到文件夹，已创建文件夹并保存！", "警告")

    def StopJudgeThread(self):
        print('JudgeThread has stopped')
        self.judgeHandle = None

    def ExitTestThread(self):
        wx.CallAfter(self.SaveTestResult)
        try:
            self.signalHandler.SendSignalCmd(self.signalHandler.GetOUTPUTCmd(1, False))
            self.signalHandler.SendSignalCmd(self.signalHandler.GetBEEPCmd())
        except ConnectionError:
            self.ConnectError(0)
        self.stop_threads = True
        self.runHandle = None
        wx.CallAfter(self.m_gaugeProcess.SetValue, 0)
        wx.CallAfter(self.m_btnStartTest.Enable)
        wx.CallAfter(self.m_btnStartTest.SetLabelText, '开始测试')
        # self.recvHandle = None
        print('MainTestThread has stopped')
        self.StopJudgeThread()

    def StopThread(self):
        try:
            self.signalHandler.SendSignalCmd(self.signalHandler.GetOUTPUTCmd(1, False))
            self.signalHandler.SendSignalCmd(self.signalHandler.GetBEEPCmd())
        except ConnectionError:
            self.ConnectError(0)
        self.stop_threads = True
        self.runHandle = None
        self.recvHandle = None
        wx.CallAfter(self.m_gaugeProcess.SetValue, 0)
        wx.CallAfter(self.m_btnStartTest.Enable)
        wx.CallAfter(self.m_btnStartTest.SetLabelText, '开始测试')
        print('MainTestThread has stopped')
        self.StopJudgeThread()

    def ConnectError(self, type=0):
        """
        连接失败，
        :param type: 0:信号发生器  1:中位机
        :return:None
        """
        if type == 0:
            wx.CallAfter(self.m_btnSignalConnect.SetLabelText, "连接信号发生器")
            wx.CallAfter(self.m_textSignalAddr.SetValue, "")
        elif type == 1:
            pass
        self.stop_threads = True
        self.runHandle = None
        self.judgeHandle = None
        wx.CallAfter(self.m_btnStartTest.Enable)
        wx.CallAfter(self.m_btnStartTest.SetLabelText, '开始测试')
        wx.CallAfter(self.SaveTestResult)
        # wx.MessageBox('已保存目前的测试结果！', '提醒')

    def SetRowValue(self, value: list):
        """
        设定测试结果表格一行的值
        :param value: 一行的值，通过列表传值
        :return: bool
        """
        if len(value) > self.m_resultGrid.GetNumberCols():
            return False
        while (self.row + 4) > self.m_resultGrid.GetNumberRows():
            self.m_resultGrid.InsertRows(-1)
        for col, v in enumerate(value):
            wx.CallAfter(self.m_resultGrid.SetCellValue, self.row, col, v)

    def OnButtonStopTestClick(self, event):
        """停止测试按钮"""
        wx.CallAfter(self.StopThread)
        event.Skip()

    def OnButtonOpenResultFolderClick(self, event):
        """打开测试结果文件夹"""
        path = '.\\log\\'
        os.startfile(path)
        event.Skip()

    def OnCkVariableParamClick(self, event):
        """
        可变参数点击事件，对按钮进行相应的enable处理
        :param event:
        :return:
        """
        eventObject = event.GetEventObject()
        self.m_radioHighVol.Enable(eventObject.GetValue())
        self.m_radioLowVol.Enable(eventObject.GetValue())
        self.m_radioRiseTime.Enable(eventObject.GetValue())
        self.m_radioDeclineTime.Enable(eventObject.GetValue())

        self.m_textMinValue.Enable(eventObject.GetValue())
        self.m_textStep.Enable(eventObject.GetValue())

        event.Skip()

    def OnRadioParamClick(self, event):
        """可变参数子项点击事件，修改相应的单位"""
        eventObject = event.GetEventObject()
        if eventObject.GetLabel() in ["高电平", "低电平"]:
            self.m_staticTextMinValueUint.SetLabelText("mV")
            self.m_staticTextStepUint.SetLabelText("mV/once")
        elif eventObject.GetLabel() in ["上升时间"]:
            riseUint = self.m_cbBoxRiseTimeUint.GetString(self.m_cbBoxRiseTimeUint.GetSelection())
            self.m_staticTextMinValueUint.SetLabelText(riseUint)
            self.m_staticTextStepUint.SetLabelText(riseUint+'/once')
        elif eventObject.GetLabel() in ["下降时间"]:
            declineUint = self.m_cbBoxRiseTimeUint.GetString(self.m_cbBoxDeclineTimeUint.GetSelection())
            self.m_staticTextMinValueUint.SetLabelText(declineUint)
            self.m_staticTextStepUint.SetLabelText(declineUint+'/once')
        event.Skip()

    def OnButtonAddTestCaseClick(self, event):
        """
        添加配置好的测试项至测试列表中
        :param event:evt
        :return:None
        """
        wx.CallAfter(self.AddTestCase2List)
        event.Skip()

    def AddTestCase2List(self):
        """
        添加测试条件
        :return:None
        """
        unitMapping = {'ns': 0, 'us': 3, 'ms': 6}
        uintRise = self.m_cbBoxRiseTimeUint.GetStringSelection()
        uintDecline = self.m_cbBoxDeclineTimeUint.GetStringSelection()

        minV = self.m_textMinValue.GetValue()
        step = self.m_textStep.GetValue()
        vHigh = self.m_textHighVol.GetValue()
        vLow = self.m_textLowVol.GetValue()
        tRise = self.m_textRiseTime.GetValue() + unitMapping.get(uintRise) * '0'
        tDecline = self.m_textDeclineTime.GetValue() + unitMapping.get(uintDecline) * '0'
        period = self.m_textPeriod.GetValue()
        times = self.m_textTimes.GetValue()
        judgeDelay = self.m_textJudgeDelay.GetValue()

        if not self.m_ckBoxIsVariable.IsChecked():  # 不可变参数
            testCase = 'Vh%s,Vl%s,Tr%s,Td%s,Tp%s,Tn%s,judgeDelay%s' % \
                       (vHigh, vLow, tRise, tDecline, period, times, judgeDelay)
        else:
            if self.m_radioHighVol.GetValue():  # 可变高电平
                testCase = 'Vh[%s_%s_%s],Vl%s,Tr%s,Td%s,Tp%s,Tn%s,judgeDelay%s' % \
                           (minV, vHigh, step, vLow, tRise, tDecline, period, times, judgeDelay)
            elif self.m_radioLowVol.GetValue():  # 可变低电平
                testCase = 'Vh%s,Vl[%s_%s_%s],Tr%s,Td%s,Tp%s,Tn%s,judgeDelay%s' % \
                           (vHigh, minV, vLow, step, tRise, tDecline, period, times, judgeDelay)
            elif self.m_radioRiseTime.GetValue():  # 可变上升沿时间
                if minV != '0':
                    minV = self.m_textMinValue.GetValue() + unitMapping.get(uintRise) * '0'
                step = self.m_textStep.GetValue() + unitMapping.get(uintRise) * '0'
                testCase = 'Vh%s,Vl%s,Tr[%s_%s_%s],Td%s,Tp%s,Tn%s,judgeDelay%s' % \
                           (vHigh, vLow, minV, tRise, step, tDecline, period, times, judgeDelay)
            elif self.m_radioDeclineTime.GetValue():  # 可变下降沿时间
                if minV != '0':
                    minV = self.m_textMinValue.GetValue() + unitMapping.get(uintDecline) * '0'
                step = self.m_textStep.GetValue() + unitMapping.get(uintDecline) * '0'
                testCase = 'Vh%s,Vl%s,Tr%s,Td[%s_%s_%s],Tp%s,Tn%s,judgeDelay%s' % \
                           (vHigh, vLow, tRise, minV, tDecline, step, period, times, judgeDelay)
            else:
                wx.MessageBox("可变参数内容未勾选！")
                return
        self.m_listTestCase.Append(testCase)

    def OnButtonClearTestCaseClick(self, event):
        """
        清空测试条件
        :param event:
        :return:None
        """
        wx.CallAfter(self.m_listTestCase.Clear)
        event.Skip()

    def OnButtonSaveTestCaseClick(self, event):
        """
        保存测试条件
        :param event:evt
        :return:None
        """
        testCase = self.m_listTestCase.GetStrings()
        dlg = wx.FileDialog(self, '保存', defaultFile='powerUdCfg.txt', defaultDir='./', wildcard='*.txt',
                            style=wx.FD_SAVE)
        if dlg.ShowModal() == wx.ID_CANCEL:
            return
        save_path = dlg.GetPath()
        try:
            with open(save_path, 'w') as f:
                f.writelines(testCase)
        except PermissionError:
            wx.MessageBox('权限不足！', '警告', parent=self)
            return
        except FileNotFoundError:
            wx.MessageBox('未找到文件!', '警告', parent=self)
            return
        wx.MessageBox('保存成功！', '提示', parent=self)
        event.Skip()

    def OnButtonLoadTestCaseClick(self, event):
        """
        加载测试条件
        :param event:evt
        :return:None
        """
        dlg = wx.FileDialog(self, '加载', defaultDir='./', wildcard='*.txt', style=wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_CANCEL:
            return
        load_path = dlg.GetPath()
        try:
            with open(load_path, 'r') as f:
                lines = f.readlines()
        except PermissionError:
            wx.MessageBox('权限不足！', '警告')
            return
        except FileNotFoundError:
            wx.MessageBox('未找到文件！', '警告')
            return
        except UnicodeDecodeError:
            wx.MessageBox('编码格式异常！')
            return
        for line in lines:
            wx.CallAfter(self.m_listTestCase.Append, line)
        event.Skip()

    def OnTimeUintcbBoxChanged(self, event):
        """
        若上升下降沿修改时间单位时可变参数选择了上升沿或下降沿，则对单位进行修改
        :param event:evt
        :return:None
        """
        eventObject = event.GetEventObject()
        if eventObject.GetToolTip() == self.m_cbBoxRiseTimeUint.GetToolTip() and self.m_radioRiseTime.GetValue():
            riseUint = self.m_cbBoxRiseTimeUint.GetString(self.m_cbBoxRiseTimeUint.GetSelection())
            self.m_staticTextMinValueUint.SetLabelText(riseUint)
            self.m_staticTextStepUint.SetLabelText(riseUint)
        elif eventObject.GetToolTip() == self.m_cbBoxDeclineTimeUint.GetToolTip() and self.m_radioDeclineTime.GetValue():
            declineUint = self.m_cbBoxRiseTimeUint.GetString(self.m_cbBoxDeclineTimeUint.GetSelection())
            self.m_staticTextMinValueUint.SetLabelText(declineUint)
            self.m_staticTextStepUint.SetLabelText(declineUint)
        event.Skip()

    def OnTestCaseDClick(self, event):
        """
        测试条件双击,删除测试条件
        :param event:
        :return:
        """
        eventObeject = event.GetEventObject()
        wx.CallAfter(eventObeject.Delete, eventObeject.GetSelection())
        event.Skip()

    def ReceiveProcess(self, evt):
        """
        从comport接收线程中将数据存入dataqueue中
        :param evt: comport.RecievData发送的evt
        :return: None
        """
        self.condition.acquire()
        print('---从comport接收的数据：' + evt.value + '------')
        self.dataQueue.put(evt.value)
        self.condition.notify()
        self.condition.release()
