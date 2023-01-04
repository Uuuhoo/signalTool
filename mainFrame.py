import wx
import Gui.guiSignal as GuiSignal
import signalPanel


# solve warning Unable to set default locale: 'unsupported locale setting'
class App(wx.App):
    def InitLocale(self):
        pass


class mainFrame(GuiSignal.mainFrame):
    def __init__(self, parent):
        GuiSignal.mainFrame.__init__(self, parent)
        self.mainPanel = signalPanel.SignalToolMainPanel(self)
        self.mainPanel.Show()
        self.Sizer.Add(self.mainPanel, 1, wx.EXPAND, 5)
        self.Sizer.Fit(self)

        self.Layout()
        self.Center(wx.BOTH)


def Main():
    app = App()
    app.MainLoop()

    mainframe = mainFrame(None)
    mainframe.Show()
    app.MainLoop()


if __name__ == '__main__':
    Main()
