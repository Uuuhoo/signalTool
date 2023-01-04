# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1-0-g8feb16b3)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.grid

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

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 799,638 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
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

		sbSizerMiddleComPort = wx.StaticBoxSizer( wx.StaticBox( sbSizerComPortSet.GetStaticBox(), wx.ID_ANY, u"主控" ), wx.VERTICAL )

		gSizerMiddleSet = wx.GridSizer( 0, 2, 0, 0 )

		self.m_textMiddlePort = wx.StaticText( sbSizerMiddleComPort.GetStaticBox(), wx.ID_ANY, u"端   口：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textMiddlePort.Wrap( -1 )

		gSizerMiddleSet.Add( self.m_textMiddlePort, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )

		m_ccMiddlePortChoices = []
		self.m_ccMiddlePort = wx.Choice( sbSizerMiddleComPort.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_ccMiddlePortChoices, 0 )
		self.m_ccMiddlePort.SetSelection( 0 )
		gSizerMiddleSet.Add( self.m_ccMiddlePort, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )

		self.m_textMiddleBaud = wx.StaticText( sbSizerMiddleComPort.GetStaticBox(), wx.ID_ANY, u"波特率：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textMiddleBaud.Wrap( -1 )

		gSizerMiddleSet.Add( self.m_textMiddleBaud, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		m_ccMiddleBaudChoices = [ u"2400", u"9600", u"19200", u"115200" ]
		self.m_ccMiddleBaud = wx.Choice( sbSizerMiddleComPort.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_ccMiddleBaudChoices, 0 )
		self.m_ccMiddleBaud.SetSelection( 0 )
		gSizerMiddleSet.Add( self.m_ccMiddleBaud, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )

		self.m_textMiddleDBitNum = wx.StaticText( sbSizerMiddleComPort.GetStaticBox(), wx.ID_ANY, u"数据位：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textMiddleDBitNum.Wrap( -1 )

		gSizerMiddleSet.Add( self.m_textMiddleDBitNum, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )

		m_ccMiddleDBitNumChoices = [ u"8", u"9" ]
		self.m_ccMiddleDBitNum = wx.Choice( sbSizerMiddleComPort.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_ccMiddleDBitNumChoices, 0 )
		self.m_ccMiddleDBitNum.SetSelection( 0 )
		gSizerMiddleSet.Add( self.m_ccMiddleDBitNum, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_textMiddleCheck = wx.StaticText( sbSizerMiddleComPort.GetStaticBox(), wx.ID_ANY, u"校验位：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textMiddleCheck.Wrap( -1 )

		gSizerMiddleSet.Add( self.m_textMiddleCheck, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )

		m_ccMiddleCheckChoices = [ u"无", u"奇校验", u"偶校验" ]
		self.m_ccMiddleCheck = wx.Choice( sbSizerMiddleComPort.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_ccMiddleCheckChoices, 0 )
		self.m_ccMiddleCheck.SetSelection( 0 )
		gSizerMiddleSet.Add( self.m_ccMiddleCheck, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_textMiddleBaud21 = wx.StaticText( sbSizerMiddleComPort.GetStaticBox(), wx.ID_ANY, u"停止位：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textMiddleBaud21.Wrap( -1 )

		gSizerMiddleSet.Add( self.m_textMiddleBaud21, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )

		m_ccMiddleStopBitChoices = [ u"1", u"1.5", u"2" ]
		self.m_ccMiddleStopBit = wx.Choice( sbSizerMiddleComPort.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_ccMiddleStopBitChoices, 0 )
		self.m_ccMiddleStopBit.SetSelection( 0 )
		gSizerMiddleSet.Add( self.m_ccMiddleStopBit, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )


		sbSizerMiddleComPort.Add( gSizerMiddleSet, 1, 0, 2 )

		self.m_btn_MiddleConnect = wx.Button( sbSizerMiddleComPort.GetStaticBox(), wx.ID_ANY, u"连接主控", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizerMiddleComPort.Add( self.m_btn_MiddleConnect, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.TOP|wx.BOTTOM, 5 )


		sbSizerComPortSet.Add( sbSizerMiddleComPort, 0, wx.EXPAND, 5 )


		leftUpSizer.Add( sbSizerComPortSet, 1, wx.EXPAND, 5 )


		leftInfoSizerMain.Add( leftUpSizer, 2, wx.EXPAND, 5 )

		leftMidSizer = wx.BoxSizer( wx.VERTICAL )

		sbSizerFuncs = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"功能区" ), wx.VERTICAL )


		leftMidSizer.Add( sbSizerFuncs, 1, wx.EXPAND, 5 )


		leftInfoSizerMain.Add( leftMidSizer, 1, wx.EXPAND, 5 )

		leftBottomSize = wx.BoxSizer( wx.VERTICAL )

		sbSizerResult = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"异常结果显示区" ), wx.VERTICAL )

		self.m_resultGrid = wx.grid.Grid( sbSizerResult.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )

		# Grid
		self.m_resultGrid.CreateGrid( 5, 4 )
		self.m_resultGrid.EnableEditing( True )
		self.m_resultGrid.EnableGridLines( True )
		self.m_resultGrid.EnableDragGridSize( False )
		self.m_resultGrid.SetMargins( 0, 0 )

		# Columns
		self.m_resultGrid.SetColSize( 0, 85 )
		self.m_resultGrid.SetColSize( 1, 88 )
		self.m_resultGrid.SetColSize( 2, 128 )
		self.m_resultGrid.SetColSize( 3, 118 )
		self.m_resultGrid.EnableDragColMove( False )
		self.m_resultGrid.EnableDragColSize( True )
		self.m_resultGrid.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Rows
		self.m_resultGrid.EnableDragRowSize( True )
		self.m_resultGrid.SetRowLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Label Appearance

		# Cell Defaults
		self.m_resultGrid.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		sbSizerResult.Add( self.m_resultGrid, 1, wx.ALL|wx.EXPAND, 5 )


		leftBottomSize.Add( sbSizerResult, 1, wx.EXPAND, 5 )


		leftInfoSizerMain.Add( leftBottomSize, 3, wx.EXPAND, 5 )


		OutterSizer.Add( leftInfoSizerMain, 3, wx.EXPAND, 5 )

		rightSetSizerMain = wx.BoxSizer( wx.VERTICAL )

		sbSizerSignalSet = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"信号发生器参数" ), wx.VERTICAL )

		setSizer = wx.GridSizer( 3, 2, 0, 0 )

		self.m_ckBoxIsVariable = wx.CheckBox( sbSizerSignalSet.GetStaticBox(), wx.ID_ANY, u"可变参数", wx.DefaultPosition, wx.DefaultSize, 0 )
		setSizer.Add( self.m_ckBoxIsVariable, 0, wx.ALL, 5 )


		setSizer.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_radioHighVol = wx.RadioButton( sbSizerSignalSet.GetStaticBox(), wx.ID_ANY, u"高电平", wx.DefaultPosition, wx.DefaultSize, 0 )
		setSizer.Add( self.m_radioHighVol, 0, wx.ALL, 5 )

		self.m_radioLowVol = wx.RadioButton( sbSizerSignalSet.GetStaticBox(), wx.ID_ANY, u"低电平", wx.DefaultPosition, wx.DefaultSize, 0 )
		setSizer.Add( self.m_radioLowVol, 0, wx.ALL, 5 )

		self.m_radioRiseTime = wx.RadioButton( sbSizerSignalSet.GetStaticBox(), wx.ID_ANY, u"上升时间", wx.DefaultPosition, wx.DefaultSize, 0 )
		setSizer.Add( self.m_radioRiseTime, 0, wx.ALL, 5 )

		self.m_radioDeclineTime = wx.RadioButton( sbSizerSignalSet.GetStaticBox(), wx.ID_ANY, u"下降时间", wx.DefaultPosition, wx.DefaultSize, 0 )
		setSizer.Add( self.m_radioDeclineTime, 0, wx.ALL, 5 )


		sbSizerSignalSet.Add( setSizer, 1, wx.EXPAND, 5 )

		setSizer1 = wx.GridSizer( 4, 3, 0, 0 )

		self.m_staticTextMinValueLabel = wx.StaticText( sbSizerSignalSet.GetStaticBox(), wx.ID_ANY, u"最小值：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextMinValueLabel.Wrap( -1 )

		setSizer1.Add( self.m_staticTextMinValueLabel, 0, wx.ALL, 5 )

		self.m_textMinValue = wx.TextCtrl( sbSizerSignalSet.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		setSizer1.Add( self.m_textMinValue, 0, wx.ALL, 5 )

		self.m_staticTextMinValue = wx.StaticText( sbSizerSignalSet.GetStaticBox(), wx.ID_ANY, u"mV/ms", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextMinValue.Wrap( -1 )

		setSizer1.Add( self.m_staticTextMinValue, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )


		sbSizerSignalSet.Add( setSizer1, 3, wx.EXPAND, 5 )

		gSizerButton = wx.GridSizer( 0, 2, 0, 0 )

		self.m_btnAddTestCase = wx.Button( sbSizerSignalSet.GetStaticBox(), wx.ID_ANY, u"添加测试条件", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizerButton.Add( self.m_btnAddTestCase, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_btnClearTestCase = wx.Button( sbSizerSignalSet.GetStaticBox(), wx.ID_ANY, u"清空测试条件", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizerButton.Add( self.m_btnClearTestCase, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_btnLoadTestCase = wx.Button( sbSizerSignalSet.GetStaticBox(), wx.ID_ANY, u"加载本地测试条件", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizerButton.Add( self.m_btnLoadTestCase, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		sbSizerSignalSet.Add( gSizerButton, 1, wx.EXPAND, 5 )


		rightSetSizerMain.Add( sbSizerSignalSet, 1, wx.EXPAND, 5 )


		OutterSizer.Add( rightSetSizerMain, 2, wx.EXPAND, 5 )


		self.SetSizer( OutterSizer )
		self.Layout()

		# Connect Events
		self.m_btnSignalConnect.Bind( wx.EVT_BUTTON, self.OnButtonSignalConnect )
		self.m_btn_MiddleConnect.Bind( wx.EVT_BUTTON, self.OnButtonMiddleConnectClick )
		self.m_btnAddTestCase.Bind( wx.EVT_BUTTON, self.OnButtonAddTestCaseClick )
		self.m_btnClearTestCase.Bind( wx.EVT_BUTTON, self.OnButtonClearTestCaseClick )
		self.m_btnLoadTestCase.Bind( wx.EVT_BUTTON, self.OnButtonLoadTestCaseClick )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def OnButtonSignalConnect( self, event ):
		event.Skip()

	def OnButtonMiddleConnectClick( self, event ):
		event.Skip()

	def OnButtonAddTestCaseClick( self, event ):
		event.Skip()

	def OnButtonClearTestCaseClick( self, event ):
		event.Skip()

	def OnButtonLoadTestCaseClick( self, event ):
		event.Skip()


