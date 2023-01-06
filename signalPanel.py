import re

import serial
import wx

import Port.comPort as ComPort
import Signal.signalHandler as SignalHandler
import Gui.guiSignal as GuiSignal
import Signal.signalCmd as signalCMD


class SignalToolMainPanel(GuiSignal.signalToolMainPanel):
    def __init__(self, parent):
        GuiSignal.signalToolMainPanel.__init__(self, parent)
        self.mainFrame = parent
        self.signalCMD = signalCMD.SignalCMD
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
        signalHandler.SendSignalCmd(self.signalCMD.Beep)
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
                wx.MessageBox("打开 " + self.m_comDlg.serialHandler.port + "失败！", "警告！", wx.OK)
                return
            self.m_btn_MiddleConnect.SetLabelText("断开主控")
        elif self.m_btn_MiddleConnect.GetLabel() == "断开主控":
            self.m_comDlg.serialHandler.close()
            self.m_btn_MiddleConnect.SetLabelText("连接主控")

    def OnButtonMiddleFlushClick(self, event):
        """刷新主控"""
        self.PortInit()

    def OnButtonClearTestResultClick(self, event):

        event.Skip()

    def OnButtonStartTestClick(self, event):

        event.Skip()

    def OnButtonStopTestClick(self, event):

        event.Skip()

    def OnButtonOpenResultFolderClick(self, event):

        event.Skip()

    def OnCkVariableParamClick(self, event):
        """可变参数点击事件，对按钮进行相应的enable处理"""
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
        """添加测试项"""
        if self.m_ckBoxIsVariable.GetValue():
            """有可变测试项"""
            # self
        event.Skip()

    def OnButtonClearTestCaseClick(self, event):

        event.Skip()

    def OnButtonSaveTestCaseClick(self, event):

        event.Skip()

    def OnButtonLoadTestCaseClick(self, event):

        event.Skip()

    def OnTimeUintcbBoxChanged(self, event):
        """若上升下降沿修改时间单位时可变参数选择了上升沿或下降沿，则对单位进行修改"""
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
        """测试项双击,删除测试项"""
        eventObeject = event.GetEventObject()
        eventObeject.Delete(eventObeject.GetSelection())
        event.Skip()
