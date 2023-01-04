# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1-0-g8feb16b3)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class mainFrame
###########################################################################

class mainFrame ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		mainSizer = wx.BoxSizer( wx.VERTICAL )


		self.SetSizer( mainSizer )
		self.Layout()

		self.Centre( wx.BOTH )

	def __del__( self ):
		pass


###########################################################################
## Class signalToolMainPanel
###########################################################################

class signalToolMainPanel ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 799,493 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		OutterSizer = wx.BoxSizer( wx.HORIZONTAL )

		leftInfoSizerMain = wx.BoxSizer( wx.VERTICAL )

		leftUpSizer = wx.BoxSizer( wx.HORIZONTAL )

		sbSizerTestItems = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"测试项" ), wx.VERTICAL )


		leftUpSizer.Add( sbSizerTestItems, 1, wx.EXPAND, 5 )

		sbSizerComPortSet = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"连接配置" ), wx.VERTICAL )

		sbSizerSignalComPort = wx.StaticBoxSizer( wx.StaticBox( sbSizerComPortSet.GetStaticBox(), wx.ID_ANY, u"信号发生器" ), wx.VERTICAL )

		gSizerSignalHandler = wx.GridSizer( 0, 2, 0, 0 )

		self.signalname = wx.StaticText( sbSizerSignalComPort.GetStaticBox(), wx.ID_ANY, u"当前信号发生器：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.signalname.Wrap( -1 )

		gSizerSignalHandler.Add( self.signalname, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_textSignalname = wx.TextCtrl( sbSizerSignalComPort.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		gSizerSignalHandler.Add( self.m_textSignalname, 0, wx.ALL, 5 )


		sbSizerSignalComPort.Add( gSizerSignalHandler, 1, wx.EXPAND, 5 )

		self.m_btnSignalConnect = wx.Button( sbSizerSignalComPort.GetStaticBox(), wx.ID_ANY, u"连接信号发生器", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizerSignalComPort.Add( self.m_btnSignalConnect, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


		sbSizerComPortSet.Add( sbSizerSignalComPort, 1, wx.EXPAND, 5 )

		sbSizerMiddleComPort = wx.StaticBoxSizer( wx.StaticBox( sbSizerComPortSet.GetStaticBox(), wx.ID_ANY, u"中位机" ), wx.VERTICAL )

		gSizerMiddleSet = wx.GridSizer( 0, 2, 0, 0 )

		self.m_textMiddlePort = wx.StaticText( sbSizerMiddleComPort.GetStaticBox(), wx.ID_ANY, u"端   口：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textMiddlePort.Wrap( -1 )

		gSizerMiddleSet.Add( self.m_textMiddlePort, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )

		m_ccMiddlePortChoices = []
		self.m_ccMiddlePort = wx.Choice( sbSizerMiddleComPort.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_ccMiddlePortChoices, 0 )
		self.m_ccMiddlePort.SetSelection( 0 )
		gSizerMiddleSet.Add( self.m_ccMiddlePort, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_textMiddleBaud = wx.StaticText( sbSizerMiddleComPort.GetStaticBox(), wx.ID_ANY, u"波特率：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textMiddleBaud.Wrap( -1 )

		gSizerMiddleSet.Add( self.m_textMiddleBaud, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		m_ccMiddleBaudChoices = []
		self.m_ccMiddleBaud = wx.Choice( sbSizerMiddleComPort.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_ccMiddleBaudChoices, 0 )
		self.m_ccMiddleBaud.SetSelection( 0 )
		gSizerMiddleSet.Add( self.m_ccMiddleBaud, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		self.m_textMiddleBaud1 = wx.StaticText( sbSizerMiddleComPort.GetStaticBox(), wx.ID_ANY, u"波特率：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textMiddleBaud1.Wrap( -1 )

		gSizerMiddleSet.Add( self.m_textMiddleBaud1, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		m_ccMiddleBaud1Choices = []
		self.m_ccMiddleBaud1 = wx.Choice( sbSizerMiddleComPort.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_ccMiddleBaud1Choices, 0 )
		self.m_ccMiddleBaud1.SetSelection( 0 )
		gSizerMiddleSet.Add( self.m_ccMiddleBaud1, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		self.m_textMiddleBaud2 = wx.StaticText( sbSizerMiddleComPort.GetStaticBox(), wx.ID_ANY, u"波特率：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textMiddleBaud2.Wrap( -1 )

		gSizerMiddleSet.Add( self.m_textMiddleBaud2, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		m_ccMiddleBaud11Choices = []
		self.m_ccMiddleBaud11 = wx.Choice( sbSizerMiddleComPort.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_ccMiddleBaud11Choices, 0 )
		self.m_ccMiddleBaud11.SetSelection( 0 )
		gSizerMiddleSet.Add( self.m_ccMiddleBaud11, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


		sbSizerMiddleComPort.Add( gSizerMiddleSet, 1, 0, 2 )

		self.m_btn_MiddleConnect = wx.Button( sbSizerMiddleComPort.GetStaticBox(), wx.ID_ANY, u"连接中位机", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizerMiddleComPort.Add( self.m_btn_MiddleConnect, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.TOP|wx.BOTTOM, 5 )


		sbSizerComPortSet.Add( sbSizerMiddleComPort, 0, wx.EXPAND, 5 )


		leftUpSizer.Add( sbSizerComPortSet, 1, wx.EXPAND, 5 )


		leftInfoSizerMain.Add( leftUpSizer, 3, wx.EXPAND, 5 )

		leftMidSizer = wx.BoxSizer( wx.VERTICAL )

		sbSizerFuncs = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"功能区" ), wx.VERTICAL )


		leftMidSizer.Add( sbSizerFuncs, 1, wx.EXPAND, 5 )


		leftInfoSizerMain.Add( leftMidSizer, 1, wx.EXPAND, 5 )

		leftBottomSize1 = wx.BoxSizer( wx.VERTICAL )

		sbSizerResult = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"结果显示区" ), wx.VERTICAL )


		leftBottomSize1.Add( sbSizerResult, 1, wx.EXPAND, 5 )


		leftInfoSizerMain.Add( leftBottomSize1, 1, wx.EXPAND, 5 )


		OutterSizer.Add( leftInfoSizerMain, 3, wx.EXPAND, 5 )

		rightSetSizerMain = wx.BoxSizer( wx.VERTICAL )

		sbSizerSignalSet = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"信号发生器参数" ), wx.VERTICAL )


		rightSetSizerMain.Add( sbSizerSignalSet, 1, wx.EXPAND, 5 )


		OutterSizer.Add( rightSetSizerMain, 1, wx.EXPAND, 5 )


		self.SetSizer( OutterSizer )
		self.Layout()

		# Connect Events
		self.m_btnSignalConnect.Bind( wx.EVT_BUTTON, self.OnButtonSignalConnect )
		self.m_btn_MiddleConnect.Bind( wx.EVT_BUTTON, self.OnButtonMiddleConnect )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def OnButtonSignalConnect( self, event ):
		event.Skip()

	def OnButtonMiddleConnect( self, event ):
		event.Skip()


