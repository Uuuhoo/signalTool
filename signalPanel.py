import re
import Port.comPort as ComPort
import Signal.signalHandler as SignalHandler
import Gui.guiSignal as GuiSignal


class SignalToolMainPanel(GuiSignal.signalToolMainPanel):
    def __init__(self, parent):
        GuiSignal.signalToolMainPanel.__init__(self, parent)
        self.mainFrame = parent

    def OnButtonSignalConnect(self, event):
        """连接信号发生器"""
        comPort = ComPort.ComPort()
        signalHandler = SignalHandler.SignalTool()

        if not signalHandler.toConnect():
            print('信号发生器连接失败！')
            return
        signalHandler.sendSignalCmd(signalHandler.signalCMD.Beep)
        signalHandler.sendSignalCmd(signalHandler.signalCMD.Output1Off)
        signalHandler.sendSignalCmd(signalHandler.signalCMD.Output1On)
        event.Skip()
