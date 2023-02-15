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


class SignalToolMainPanel(GuiSignal.signalToolMainPanel):
    def __init__(self, parent):
        GuiSignal.signalToolMainPanel.__init__(self, parent)
        self.mainFrame = parent
        self.row = 1
        self.comPort = ComPort.ComPort()
        self.runHandle = None
        self.recvHandle = None
        self.condition = threading.Condition()
        self.dataQueue = queue.Queue()
        self.stop_threads = False  # 停止线程标识
        self.schedule = sched.scheduler(time.time, time.sleep)
        self.Bind(ComPort.EVT_DATA, self.ReceiveProcess)
        self.signalHandler = SignalHandler.SignalTool()
        self.PortInit()

    def PortInit(self):
        """
        刷新端口列表并显示
        :return:
        """
        wx.CallAfter(self.m_ccMiddlePort.SetItems, list(self.comPort.GetFlushComPorts().keys()))
        wx.CallAfter(self.m_ccMiddlePort.SetSelection, 0)

    def OnButtonSignalConnectClick(self, event) -> None:
        """连接信号发生器"""
        if not self.signalHandler.DoConnect():
            wx.MessageBox("信号发生器连接失败，请检查连接状态！", "Warning!")
            wx.CallAfter(self.m_textSignalAddr.SetValue, "")
            wx.CallAfter(self.m_btnSignalConnect.SetLabelText, "连接信号发生器")
            print('信号发生器连接失败！')
            return
        self.signalHandler.SendSignalCmd(self.signalHandler.GetBEEPCmd())
        wx.CallAfter(self.m_textSignalAddr.SetValue, self.signalHandler.signalInfo.GetNowAddr())
        wx.CallAfter(self.m_btnSignalConnect.SetLabelText, "已连接信号发生器")
        event.Skip()

    def OnButtonMiddleConnectClick(self, event):
        """连接主控点击事件"""
        self.ConnectMainControl()
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
        wx.MilliSleep(50)

        self.comPort.serialHandler.port = port
        self.comPort.serialHandler.baudrate = baud
        self.comPort.serialHandler.parity = Parity[check]
        self.comPort.serialHandler.bytesize = DataBits[bitsize]
        self.comPort.serialHandler.stopbits = StopBits[stopsize]
        self.comPort.timeout = 0

        if self.m_btn_MiddleConnect.GetLabel() == "连接主控":
            try:
                self.comPort.serialHandler.open()
                wx.MilliSleep(50)
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
        self.row = 1
        event.Skip()

    def OnButtonStartTestClick(self, event):
        """开始测试按钮"""
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
                         cmdType.LowHighStep: cmdAnalysed.GetLowHighStepValue()
                         })
            testQueue.append(copy.deepcopy(tempItem))

        # 根据解析完的命令依次进行测试
        for i in range(len(testQueue)):
            if stop_threads():
                self.stopThread()
                return
            nowTest = testQueue[i]
            if nowTest.get(cmdType.VariableParamName) == cmdType.Vh:
                pass
            if nowTest.get(cmdType.VariableParamName) == cmdType.Vl:
                lvs = nowTest.get(cmdType.LowHighStep)
                low = float(lvs[0])
                high = float(lvs[1])
                step = float(lvs[2])

                while low <= high:
                    # self.signalHandler.SendSignalCmd(self.signalHandler.GetOUTPUTCmd(1, False))  # 关闭通道1
                    # self.signalHandler.SendSignalCmd(self.signalHandler.GetFUNCCmd(1, 'PULS'))  # 设置波形为脉冲
                    # self.signalHandler.SendSignalCmd(
                    #     self.signalHandler.GetVOLTHighCmd(1, nowTest.get(cmdType.Vh)))  # 高电平
                    # self.signalHandler.SendSignalCmd(self.signalHandler.GetVOLTLowCmd(1, str(low)))  # 低电平
                    # self.signalHandler.SendSignalCmd(self.signalHandler.GetTRiseCmd(1, nowTest.get(cmdType.Tr)))  # 上升沿
                    # self.signalHandler.SendSignalCmd(
                    #     self.signalHandler.GetTDeclineCmd(1, nowTest.get(cmdType.Td)))  # 下降沿
                    # self.signalHandler.SendSignalCmd(self.signalHandler.GetPULSPerCmd(1, nowTest.get(cmdType.Tp)))  # 周期
                    # self.signalHandler.SendSignalCmd(self.signalHandler.GetDCYCCmd(1, '50'))  # 占空比
                    # self.signalHandler.SendSignalCmd(self.signalHandler.GetPHASCmd(1, '0'))  # 相位
                    # self.signalHandler.SendSignalCmd(self.signalHandler.GetOUTPUTCmd(1, True))  # 开启通道1
                    print('-------start time:' + str(time.time()))
                    self.schedule.enter(0.4, 1, self.CheckResult, )
                    for _ in range(int(nowTest.get(cmdType.Tn))-1):
                        if self.recvHandle is not None:
                            pass
                        self.schedule.enter(float(nowTest.get(cmdType.Tp)), 1, self.Task4Check, )
                        self.schedule.run()
                    low += step

                    print('-------finished time:' + str(time.time()))
            if nowTest.get(cmdType.VariableParamName) == cmdType.Tr:
                pass
            if nowTest.get(cmdType.VariableParamName) == cmdType.Td:
                pass
            freq = nowTest.get(cmdType.Tn)

        self.stopThread()

    def Task4Check(self):
        self.schedule.enter(0.4, 1, self.CheckResult, )     # 用线程实现
        self.schedule.run()
        # self.CheckResult()
        # wx.CallLater(400, self.CheckResult)

    def CheckResult(self):
        # self.comPort.SendData('5A')
        print('run task time:' + str(time.time()))

    def stopThread(self):
        self.stop_threads = True
        self.runHandle = None
        self.recvHandle = None

    def OnButtonStopTestClick(self, event):
        """停止测试按钮"""
        self.stop_threads = True
        self.runHandle = None
        self.recvHandle = None
        event.Skip()

    def OnButtonOpenResultFolderClick(self, event):
        """打开测试结果文件夹"""
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
            self.m_staticTextMinValueUint.SetLabelText("mV/ms")
            self.m_staticTextStepUint.SetLabelText("mV/ms")
        elif eventObject.GetLabel() in ["上升时间"]:
            riseUint = self.m_cbBoxRiseTimeUint.GetString(self.m_cbBoxRiseTimeUint.GetSelection())
            self.m_staticTextMinValueUint.SetLabelText(riseUint)
            self.m_staticTextStepUint.SetLabelText(riseUint)
        elif eventObject.GetLabel() in ["下降时间"]:
            declineUint = self.m_cbBoxRiseTimeUint.GetString(self.m_cbBoxDeclineTimeUint.GetSelection())
            self.m_staticTextMinValueUint.SetLabelText(declineUint)
            self.m_staticTextStepUint.SetLabelText(declineUint)
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

        if not self.m_ckBoxIsVariable.IsChecked():  # 不可变参数
            testCase = 'Vh%s,Vl%s,Tr%s,Td%s,Tp%s,Tn%s' % \
                       (vHigh, vLow, tRise, tDecline, period, times)
        else:
            if self.m_radioHighVol.GetValue():  # 可变高电平
                testCase = 'Vh[%s_%s_%s],Vl%s,Tr%s,Td%s,Tp%s,Tn%s' % \
                           (minV, vHigh, step, vLow, tRise, tDecline, period, times)
            elif self.m_radioLowVol.GetValue():  # 可变低电平
                testCase = 'Vh%s,Vl[%s_%s_%s],Tr%s,Td%s,Tp%s,Tn%s' % \
                           (vHigh, minV, vLow, step, tRise, tDecline, period, times)
            elif self.m_radioRiseTime.GetValue():  # 可变上升沿时间
                if minV != '0':
                    minV = self.m_textMinValue.GetValue() + unitMapping.get(uintRise) * '0'
                step = self.m_textStep.GetValue() + unitMapping.get(uintRise) * '0'
                testCase = 'Vh%s,Vl%s,Tr[%s_%s_%s],Td%s,Tp%s,Tn%s' % \
                           (vHigh, vLow, minV, tRise, step, tDecline, period, times)
            elif self.m_radioDeclineTime.GetValue():  # 可变下降沿时间
                if minV != '0':
                    minV = self.m_textMinValue.GetValue() + unitMapping.get(uintDecline) * '0'
                step = self.m_textStep.GetValue() + unitMapping.get(uintDecline) * '0'
                testCase = 'Vh%s,Vl%s,Tr%s,Td[%s_%s_%s],Tp%s,Tn%s' % \
                           (vHigh, vLow, tRise, minV, tDecline, step, period, times)
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
        dlg = wx.FileDialog(self, '保存', defaultFile='powerUdCfg', defaultDir='./', wildcard='*.txt', style=wx.FD_SAVE)
        if dlg.ShowModal() == wx.ID_CANCEL:
            return
        save_path = dlg.GetPath()
        try:
            with open(save_path, 'w') as f:
                f.writelines(testCase)
        except PermissionError:
            wx.MessageBox('权限不足！', '警告', parent=self)
        except FileNotFoundError:
            wx.MessageBox('未找到文件!', '警告', parent=self)
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
        except FileNotFoundError:
            wx.MessageBox('未找到文件！', '警告')
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
