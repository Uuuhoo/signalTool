import re

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
        comPort = ComPort.ComPort()
        self.m_ccMiddlePort.SetItems(comPort.comPorts)
        # comPort.comPorts
        event.Skip()

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


