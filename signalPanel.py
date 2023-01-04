import re
import Port.comPort as ComPort
import Signal.signalHandler as SignalHandler
import Gui.guiSignal as GuiSignal
import Signal.signalCmd as signalCMD


class SignalToolMainPanel(GuiSignal.signalToolMainPanel):
    def __init__(self, parent):
        GuiSignal.signalToolMainPanel.__init__(self, parent)
        self.mainFrame = parent
        self.signalCMD = signalCMD.SignalCMD

    def OnButtonSignalConnect(self, event) -> None:
        """连接信号发生器"""
        comPort = ComPort.ComPort()
        signalHandler = SignalHandler.SignalTool()
        if not signalHandler.DoConnect():
            print('信号发生器连接失败！')
            return
        signalHandler.SendSignalCmd(self.signalCMD.Beep)
        event.Skip()


