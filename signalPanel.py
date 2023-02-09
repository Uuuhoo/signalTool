import re

import serial
import wx

import Port.comPort as ComPort
import Signal.signalHandler as SignalHandler
import Gui.guiSignal as GuiSignal


class SignalToolMainPanel(GuiSignal.signalToolMainPanel):
    def __init__(self, parent):
        GuiSignal.signalToolMainPanel.__init__(self, parent)
        self.mainFrame = parent
        self.row = 1
        self.m_comDlg = ComPort.ComPort()
        self.PortInit()

    def PortInit(self):
        self.m_ccMiddlePort.SetItems(list(self.m_comDlg.GetFlushComPorts().keys()))
        self.m_ccMiddlePort.SetSelection(0)

    def OnButtonSignalConnectClick(self, event) -> None:
        """连接信号发生器"""
        signalHandler = SignalHandler.SignalTool()
        if not signalHandler.DoConnect():
            wx.MessageBox("信号发生器连接失败，请检查连接状态！", "Warning!")
            print('信号发生器连接失败！')
            return
        signalHandler.SendSignalCmd(signalHandler.GetBEEPCmd())
        self.m_textSignalAddr.SetValue(signalHandler.signalInfo.GetNowAddr())
        event.Skip()

    def OnButtonMiddleConnectClick(self, event):
        """连接主控点击事件"""
        self.ConnectMainControl()
        event.Skip()

    def ConnectMainControl(self):
        """连接主控"""
        port = self.m_comDlg.GetFlushComPorts().get(self.m_ccMiddlePort.GetStringSelection())
        baud = int(self.m_ccMiddleBaud.GetStringSelection())
        bitsize = self.m_ccMiddleDBitNum.GetStringSelection()
        check = self.m_ccMiddleCheck.GetStringSelection()
        check = 'None'  # 固定不校验
        stopsize = self.m_ccMiddleStopBit.GetStringSelection()

        Parity = {'None': 'N', 'Even': 'E', 'Odd': 'O'}
        DataBits = {'5': 5, '6': 6, '7': 7, '8': 8}
        StopBits = {'1': 1, '1.5': 1.5, '2': 2}
        self.m_comDlg.serialHandler.close()
        wx.MilliSleep(50)

        self.m_comDlg.serialHandler.port = port
        self.m_comDlg.serialHandler.baudrate = baud
        self.m_comDlg.serialHandler.parity = Parity[check]
        self.m_comDlg.serialHandler.bytesize = DataBits[bitsize]
        self.m_comDlg.serialHandler.stopbits = StopBits[stopsize]
        self.m_comDlg.timeout = 0

        if self.m_btn_MiddleConnect.GetLabel() == "连接主控":
            try:
                self.m_comDlg.serialHandler.open()
                wx.MilliSleep(50)
            except serial.SerialException:
                wx.MessageBox("打开 " + str(self.m_comDlg.serialHandler.port) + "失败！", "警告！", wx.OK)
                return
            wx.CallAfter(self.m_btn_MiddleConnect.SetLabelText, "断开主控")
        elif self.m_btn_MiddleConnect.GetLabel() == "断开主控":
            self.m_comDlg.serialHandler.close()
            wx.CallAfter(self.m_btn_MiddleConnect.SetLabelText, "连接主控")

    def OnButtonMiddleFlushClick(self, event):
        """刷新主控接口"""
        wx.CallAfter(self.PortInit)

    def OnButtonClearTestResultClick(self, event):
        wx.CallAfter(self.m_resultGrid.ClearGrid)
        self.row = 1
        event.Skip()

    def OnButtonStartTestClick(self, event):

        event.Skip()

    def OnButtonStopTestClick(self, event):

        event.Skip()

    def OnButtonOpenResultFolderClick(self, event):

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

        if not self.m_ckBoxIsVariable.IsChecked():    # 不可变参数
            testCase = 'Vh%s,Vl%s,Tr%s,Td%s,Tp%s,Tn%s' % \
                       (vHigh, vLow, tRise, tDecline, period, times)
        else:
            if self.m_radioHighVol.GetValue():  # 可变高电平
                testCase = 'Vh[%s,%s,%s],Vl%s,Tr%s,Td%s,Tp%s,Tn%s' % \
                           (minV, vHigh, step, vLow, tRise, tDecline, period, times)
            elif self.m_radioLowVol.GetValue():  # 可变低电平
                testCase = 'Vh%s,Vl[%s,%s,%s],Tr%s,Td%s,Tp%s,Tn%s' % \
                           (vHigh, minV, vLow, step, tRise, tDecline, period, times)
            elif self.m_radioRiseTime.GetValue():  # 可变上升沿时间
                if minV != '0':
                    minV = self.m_textMinValue.GetValue() + unitMapping.get(uintRise) * '0'
                step = self.m_textStep.GetValue() + unitMapping.get(uintRise) * '0'
                testCase = 'Vh%s,Vl%s,Tr[%s,%s,%s],Td%s,Tp%s,Tn%s' % \
                           (vHigh, vLow, minV, tRise, step, tDecline, period, times)
            elif self.m_radioDeclineTime.GetValue():  # 可变下降沿时间
                if minV != '0':
                    minV = self.m_textMinValue.GetValue() + unitMapping.get(uintDecline) * '0'
                step = self.m_textStep.GetValue() + unitMapping.get(uintDecline) * '0'
                testCase = 'Vh%s,Vl%s,Tr%s,Td[%s,%s,%s],Tp%s,Tn%s' % \
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
        eventObeject.Delete(eventObeject.GetSelection())
        event.Skip()
