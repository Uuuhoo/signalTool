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

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 799,624 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		OutterSizer = wx.BoxSizer( wx.HORIZONTAL )

		self.m_splitterOutter = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.m_splitterOutter.SetSashGravity( 0.5 )
		self.m_splitterOutter.Bind( wx.EVT_IDLE, self.m_splitterOutterOnIdle )

		self.m_leftpanel = wx.Panel( self.m_splitterOutter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		leftInfoSizerMain = wx.BoxSizer( wx.VERTICAL )

		leftUpSizer = wx.BoxSizer( wx.HORIZONTAL )

		self.m_splitterTestCaseAndComPort = wx.SplitterWindow( self.m_leftpanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.m_splitterTestCaseAndComPort.Bind( wx.EVT_IDLE, self.m_splitterTestCaseAndComPortOnIdle )

		self.m_panelTestCase = wx.Panel( self.m_splitterTestCaseAndComPort, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sbSizerTestCase = wx.StaticBoxSizer( wx.StaticBox( self.m_panelTestCase, wx.ID_ANY, u"测试项" ), wx.VERTICAL )

		m_listTestCaseChoices = [ u"很大声的", u"大萨达撒" ]
		self.m_listTestCase = wx.ListBox( sbSizerTestCase.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_listTestCaseChoices, 0 )
		sbSizerTestCase.Add( self.m_listTestCase, 1, wx.EXPAND|wx.ALL, 5 )


		self.m_panelTestCase.SetSizer( sbSizerTestCase )
		self.m_panelTestCase.Layout()
		sbSizerTestCase.Fit( self.m_panelTestCase )
		self.m_panelComPort = wx.Panel( self.m_splitterTestCaseAndComPort, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sbSizerComPortSet = wx.StaticBoxSizer( wx.StaticBox( self.m_panelComPort, wx.ID_ANY, u"连接配置" ), wx.VERTICAL )

		sbSizerSignalComPort = wx.StaticBoxSizer( wx.StaticBox( sbSizerComPortSet.GetStaticBox(), wx.ID_ANY, u"信号发生器" ), wx.VERTICAL )

		fgSizerSignalSet = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizerSignalSet.SetFlexibleDirection( wx.BOTH )
		fgSizerSignalSet.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.signalname = wx.StaticText( sbSizerSignalComPort.GetStaticBox(), wx.ID_ANY, u"SignalAddr：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.signalname.Wrap( -1 )

		fgSizerSignalSet.Add( self.signalname, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_textSignalAddr = wx.TextCtrl( sbSizerSignalComPort.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		fgSizerSignalSet.Add( self.m_textSignalAddr, 0, wx.ALL, 5 )


		sbSizerSignalComPort.Add( fgSizerSignalSet, 1, wx.EXPAND, 5 )

		self.m_btnSignalConnect = wx.Button( sbSizerSignalComPort.GetStaticBox(), wx.ID_ANY, u"连接信号发生器", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizerSignalComPort.Add( self.m_btnSignalConnect, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.BOTTOM, 5 )


		sbSizerComPortSet.Add( sbSizerSignalComPort, 0, wx.EXPAND, 5 )

		sbSizerMiddleComPort = wx.StaticBoxSizer( wx.StaticBox( sbSizerComPortSet.GetStaticBox(), wx.ID_ANY, u"主控" ), wx.VERTICAL )

		fgSizerPortSet = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizerPortSet.SetFlexibleDirection( wx.HORIZONTAL )
		fgSizerPortSet.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_textMiddlePort = wx.StaticText( sbSizerMiddleComPort.GetStaticBox(), wx.ID_ANY, u"端   口：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textMiddlePort.Wrap( -1 )

		fgSizerPortSet.Add( self.m_textMiddlePort, 0, wx.ALIGN_CENTER_VERTICAL, 5 )

		m_ccMiddlePortChoices = []
		self.m_ccMiddlePort = wx.Choice( sbSizerMiddleComPort.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size( 135,-1 ), m_ccMiddlePortChoices, 0 )
		self.m_ccMiddlePort.SetSelection( 0 )
		fgSizerPortSet.Add( self.m_ccMiddlePort, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 5 )

		self.m_textMiddleBaud = wx.StaticText( sbSizerMiddleComPort.GetStaticBox(), wx.ID_ANY, u"波特率：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textMiddleBaud.Wrap( -1 )

		fgSizerPortSet.Add( self.m_textMiddleBaud, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		m_ccMiddleBaudChoices = [ u"2400", u"9600", u"19200", u"115200" ]
		self.m_ccMiddleBaud = wx.Choice( sbSizerMiddleComPort.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_ccMiddleBaudChoices, 0 )
		self.m_ccMiddleBaud.SetSelection( 1 )
		fgSizerPortSet.Add( self.m_ccMiddleBaud, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND|wx.LEFT, 5 )

		self.m_textMiddleDBitNum = wx.StaticText( sbSizerMiddleComPort.GetStaticBox(), wx.ID_ANY, u"数据位：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textMiddleDBitNum.Wrap( -1 )

		fgSizerPortSet.Add( self.m_textMiddleDBitNum, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )

		m_ccMiddleDBitNumChoices = [ u"8", u"9" ]
		self.m_ccMiddleDBitNum = wx.Choice( sbSizerMiddleComPort.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_ccMiddleDBitNumChoices, 0 )
		self.m_ccMiddleDBitNum.SetSelection( 0 )
		fgSizerPortSet.Add( self.m_ccMiddleDBitNum, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

		self.m_textMiddleCheck = wx.StaticText( sbSizerMiddleComPort.GetStaticBox(), wx.ID_ANY, u"校验位：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textMiddleCheck.Wrap( -1 )

		fgSizerPortSet.Add( self.m_textMiddleCheck, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )

		m_ccMiddleCheckChoices = [ u"None", u"Odd", u"Even" ]
		self.m_ccMiddleCheck = wx.Choice( sbSizerMiddleComPort.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_ccMiddleCheckChoices, 0 )
		self.m_ccMiddleCheck.SetSelection( 0 )
		fgSizerPortSet.Add( self.m_ccMiddleCheck, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

		self.m_textMiddleBaud21 = wx.StaticText( sbSizerMiddleComPort.GetStaticBox(), wx.ID_ANY, u"停止位：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textMiddleBaud21.Wrap( -1 )

		fgSizerPortSet.Add( self.m_textMiddleBaud21, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )

		m_ccMiddleStopBitChoices = [ u"1", u"1.5", u"2" ]
		self.m_ccMiddleStopBit = wx.Choice( sbSizerMiddleComPort.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_ccMiddleStopBitChoices, 0 )
		self.m_ccMiddleStopBit.SetSelection( 0 )
		fgSizerPortSet.Add( self.m_ccMiddleStopBit, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )


		sbSizerMiddleComPort.Add( fgSizerPortSet, 1, wx.EXPAND, 5 )

		bSizerMiddleControl = wx.BoxSizer( wx.HORIZONTAL )

		self.m_btn_MiddleFlush = wx.Button( sbSizerMiddleComPort.GetStaticBox(), wx.ID_ANY, u"刷新串口", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizerMiddleControl.Add( self.m_btn_MiddleFlush, 0, wx.ALL, 5 )

		self.m_btn_MiddleConnect = wx.Button( sbSizerMiddleComPort.GetStaticBox(), wx.ID_ANY, u"连接主控", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizerMiddleControl.Add( self.m_btn_MiddleConnect, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.TOP, 5 )


		sbSizerMiddleComPort.Add( bSizerMiddleControl, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )


		sbSizerComPortSet.Add( sbSizerMiddleComPort, 0, wx.EXPAND, 5 )


		self.m_panelComPort.SetSizer( sbSizerComPortSet )
		self.m_panelComPort.Layout()
		sbSizerComPortSet.Fit( self.m_panelComPort )
		self.m_splitterTestCaseAndComPort.SplitVertically( self.m_panelTestCase, self.m_panelComPort, 300 )
		leftUpSizer.Add( self.m_splitterTestCaseAndComPort, 1, wx.EXPAND, 5 )


		leftInfoSizerMain.Add( leftUpSizer, 0, wx.EXPAND, 5 )

		leftMidSizer = wx.BoxSizer( wx.VERTICAL )

		sbSizerFuncs = wx.StaticBoxSizer( wx.StaticBox( self.m_leftpanel, wx.ID_ANY, u"功能区" ), wx.VERTICAL )

		gSizerControl = wx.GridSizer( 1, 4, 0, 0 )

		self.m_btnClearResult = wx.Button( sbSizerFuncs.GetStaticBox(), wx.ID_ANY, u"清空结果", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizerControl.Add( self.m_btnClearResult, 0, wx.LEFT, 5 )

		self.m_btnStartTest = wx.Button( sbSizerFuncs.GetStaticBox(), wx.ID_ANY, u"开始测试", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizerControl.Add( self.m_btnStartTest, 0, 0, 5 )

		self.m_btnStopTest = wx.Button( sbSizerFuncs.GetStaticBox(), wx.ID_ANY, u"停止测试", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizerControl.Add( self.m_btnStopTest, 0, 0, 5 )

		self.m_btnOpenResultFolder = wx.Button( sbSizerFuncs.GetStaticBox(), wx.ID_ANY, u"打开测试结果", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizerControl.Add( self.m_btnOpenResultFolder, 0, 0, 5 )


		sbSizerFuncs.Add( gSizerControl, 1, wx.EXPAND, 5 )

		bSizerProgress = wx.BoxSizer( wx.VERTICAL )

		self.m_gauge1 = wx.Gauge( sbSizerFuncs.GetStaticBox(), wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
		self.m_gauge1.SetValue( 0 )
		bSizerProgress.Add( self.m_gauge1, 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 5 )


		sbSizerFuncs.Add( bSizerProgress, 0, wx.EXPAND, 5 )


		leftMidSizer.Add( sbSizerFuncs, 1, wx.EXPAND, 5 )


		leftInfoSizerMain.Add( leftMidSizer, 0, wx.EXPAND, 5 )

		leftBottomSize = wx.BoxSizer( wx.VERTICAL )

		sbSizerResult = wx.StaticBoxSizer( wx.StaticBox( self.m_leftpanel, wx.ID_ANY, u"异常结果显示区" ), wx.VERTICAL )

		self.m_resultGrid = wx.grid.Grid( sbSizerResult.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )

		# Grid
		self.m_resultGrid.CreateGrid( 5, 4 )
		self.m_resultGrid.EnableEditing( True )
		self.m_resultGrid.EnableGridLines( True )
		self.m_resultGrid.EnableDragGridSize( True )
		self.m_resultGrid.SetMargins( 0, 0 )

		# Columns
		self.m_resultGrid.SetColSize( 0, 85 )
		self.m_resultGrid.SetColSize( 1, 88 )
		self.m_resultGrid.SetColSize( 2, 114 )
		self.m_resultGrid.SetColSize( 3, 110 )
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


		leftInfoSizerMain.Add( leftBottomSize, 4, wx.EXPAND, 5 )


		self.m_leftpanel.SetSizer( leftInfoSizerMain )
		self.m_leftpanel.Layout()
		leftInfoSizerMain.Fit( self.m_leftpanel )
		self.m_rightpanel = wx.Panel( self.m_splitterOutter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		rightSetSizerMain = wx.BoxSizer( wx.VERTICAL )

		sbSizerSignalSet = wx.StaticBoxSizer( wx.StaticBox( self.m_rightpanel, wx.ID_ANY, u"信号发生器参数" ), wx.VERTICAL )

		setSizer = wx.GridSizer( 3, 2, 0, 0 )

		self.m_ckBoxIsVariable = wx.CheckBox( sbSizerSignalSet.GetStaticBox(), wx.ID_ANY, u"可变参数", wx.DefaultPosition, wx.DefaultSize, 0 )
		setSizer.Add( self.m_ckBoxIsVariable, 0, wx.ALL, 5 )


		setSizer.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_radioHighVol = wx.RadioButton( sbSizerSignalSet.GetStaticBox(), wx.ID_ANY, u"高电平", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_radioHighVol.Enable( False )

		setSizer.Add( self.m_radioHighVol, 0, wx.ALL, 5 )

		self.m_radioLowVol = wx.RadioButton( sbSizerSignalSet.GetStaticBox(), wx.ID_ANY, u"低电平", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_radioLowVol.Enable( False )

		setSizer.Add( self.m_radioLowVol, 0, wx.ALL, 5 )

		self.m_radioRiseTime = wx.RadioButton( sbSizerSignalSet.GetStaticBox(), wx.ID_ANY, u"上升时间", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_radioRiseTime.Enable( False )

		setSizer.Add( self.m_radioRiseTime, 0, wx.ALL, 5 )

		self.m_radioDeclineTime = wx.RadioButton( sbSizerSignalSet.GetStaticBox(), wx.ID_ANY, u"下降时间", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_radioDeclineTime.Enable( False )

		setSizer.Add( self.m_radioDeclineTime, 0, wx.ALL, 5 )


		sbSizerSignalSet.Add( setSizer, 0, wx.EXPAND, 5 )

		self.m_staticline1 = wx.StaticLine( sbSizerSignalSet.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		sbSizerSignalSet.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )

		setSizer1 = wx.GridSizer( 8, 3, 0, 0 )

		self.m_staticTextMinValueLabel = wx.StaticText( sbSizerSignalSet.GetStaticBox(), wx.ID_ANY, u"最小值：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextMinValueLabel.Wrap( -1 )

		setSizer1.Add( self.m_staticTextMinValueLabel, 0, wx.ALL, 5 )

		self.m_textMinValue = wx.TextCtrl( sbSizerSignalSet.GetStaticBox(), wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textMinValue.Enable( False )

		setSizer1.Add( self.m_textMinValue, 0, wx.ALL, 5 )

		self.m_staticTextMinValueUint = wx.StaticText( sbSizerSignalSet.GetStaticBox(), wx.ID_ANY, u"mV/ms", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextMinValueUint.Wrap( -1 )

		setSizer1.Add( self.m_staticTextMinValueUint, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )

		self.m_staticTextStepLabel = wx.StaticText( sbSizerSignalSet.GetStaticBox(), wx.ID_ANY, u"步长：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextStepLabel.Wrap( -1 )

		setSizer1.Add( self.m_staticTextStepLabel, 0, wx.ALL, 5 )

		self.m_textStep = wx.TextCtrl( sbSizerSignalSet.GetStaticBox(), wx.ID_ANY, u"10", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textStep.Enable( False )

		setSizer1.Add( self.m_textStep, 0, wx.ALL, 5 )

		self.m_staticTextStepUint = wx.StaticText( sbSizerSignalSet.GetStaticBox(), wx.ID_ANY, u"mV/ms", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextStepUint.Wrap( -1 )

		setSizer1.Add( self.m_staticTextStepUint, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )

		self.m_staticTextHighVolLabel = wx.StaticText( sbSizerSignalSet.GetStaticBox(), wx.ID_ANY, u"高电平：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextHighVolLabel.Wrap( -1 )

		setSizer1.Add( self.m_staticTextHighVolLabel, 0, wx.ALL, 5 )

		self.m_textHighVol = wx.TextCtrl( sbSizerSignalSet.GetStaticBox(), wx.ID_ANY, u"5000", wx.DefaultPosition, wx.DefaultSize, 0 )
		setSizer1.Add( self.m_textHighVol, 0, wx.ALL, 5 )

		self.m_staticHighVolUint = wx.StaticText( sbSizerSignalSet.GetStaticBox(), wx.ID_ANY, u"mV", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticHighVolUint.Wrap( -1 )

		setSizer1.Add( self.m_staticHighVolUint, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )

		self.m_staticTextLowVolLabel = wx.StaticText( sbSizerSignalSet.GetStaticBox(), wx.ID_ANY, u"低电平：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextLowVolLabel.Wrap( -1 )

		setSizer1.Add( self.m_staticTextLowVolLabel, 0, wx.ALL, 5 )

		self.m_textLowVol = wx.TextCtrl( sbSizerSignalSet.GetStaticBox(), wx.ID_ANY, u"1200", wx.DefaultPosition, wx.DefaultSize, 0 )
		setSizer1.Add( self.m_textLowVol, 0, wx.ALL, 5 )

		self.m_staticTextLowVolUint = wx.StaticText( sbSizerSignalSet.GetStaticBox(), wx.ID_ANY, u"mV", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextLowVolUint.Wrap( -1 )

		setSizer1.Add( self.m_staticTextLowVolUint, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )

		self.m_staticRiseTimeLabel = wx.StaticText( sbSizerSignalSet.GetStaticBox(), wx.ID_ANY, u"上升时间：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticRiseTimeLabel.Wrap( -1 )

		setSizer1.Add( self.m_staticRiseTimeLabel, 0, wx.ALL, 5 )

		self.m_textRiseTime = wx.TextCtrl( sbSizerSignalSet.GetStaticBox(), wx.ID_ANY, u"50", wx.DefaultPosition, wx.DefaultSize, 0 )
		setSizer1.Add( self.m_textRiseTime, 0, wx.ALL, 5 )

		m_cbBoxRiseTimeUintChoices = [ u"ns", u"us", u"ms" ]
		self.m_cbBoxRiseTimeUint = wx.ComboBox( sbSizerSignalSet.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, m_cbBoxRiseTimeUintChoices, wx.CB_READONLY )
		self.m_cbBoxRiseTimeUint.SetSelection( 0 )
		self.m_cbBoxRiseTimeUint.SetToolTip( u"RiseTimeUint" )

		setSizer1.Add( self.m_cbBoxRiseTimeUint, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )

		self.m_staticTextDeclineTimeLabel = wx.StaticText( sbSizerSignalSet.GetStaticBox(), wx.ID_ANY, u"下降时间：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextDeclineTimeLabel.Wrap( -1 )

		setSizer1.Add( self.m_staticTextDeclineTimeLabel, 0, wx.ALL, 5 )

		self.m_textDeclineTime = wx.TextCtrl( sbSizerSignalSet.GetStaticBox(), wx.ID_ANY, u"50", wx.DefaultPosition, wx.DefaultSize, 0 )
		setSizer1.Add( self.m_textDeclineTime, 0, wx.ALL, 5 )

		m_cbBoxDeclineTimeUintChoices = [ u"ns", u"us", u"ms" ]
		self.m_cbBoxDeclineTimeUint = wx.ComboBox( sbSizerSignalSet.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, m_cbBoxDeclineTimeUintChoices, wx.CB_READONLY )
		self.m_cbBoxDeclineTimeUint.SetSelection( 0 )
		self.m_cbBoxDeclineTimeUint.SetToolTip( u"DeclineTimeUint" )

		setSizer1.Add( self.m_cbBoxDeclineTimeUint, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )

		self.m_staticTextPeriodLabel = wx.StaticText( sbSizerSignalSet.GetStaticBox(), wx.ID_ANY, u"周期：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextPeriodLabel.Wrap( -1 )

		setSizer1.Add( self.m_staticTextPeriodLabel, 0, wx.ALL, 5 )

		self.m_textPeriod = wx.TextCtrl( sbSizerSignalSet.GetStaticBox(), wx.ID_ANY, u"1000", wx.DefaultPosition, wx.DefaultSize, 0 )
		setSizer1.Add( self.m_textPeriod, 0, wx.ALL, 5 )

		self.m_staticTextPeriodUint = wx.StaticText( sbSizerSignalSet.GetStaticBox(), wx.ID_ANY, u"ms", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextPeriodUint.Wrap( -1 )

		setSizer1.Add( self.m_staticTextPeriodUint, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )

		self.m_staticTextTimesLabel = wx.StaticText( sbSizerSignalSet.GetStaticBox(), wx.ID_ANY, u"循环次数：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextTimesLabel.Wrap( -1 )

		setSizer1.Add( self.m_staticTextTimesLabel, 0, wx.ALL, 5 )

		self.m_textTimes = wx.TextCtrl( sbSizerSignalSet.GetStaticBox(), wx.ID_ANY, u"6", wx.DefaultPosition, wx.DefaultSize, 0 )
		setSizer1.Add( self.m_textTimes, 0, wx.ALL, 5 )

		self.m_staticTextTimesUint = wx.StaticText( sbSizerSignalSet.GetStaticBox(), wx.ID_ANY, u"次", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextTimesUint.Wrap( -1 )

		setSizer1.Add( self.m_staticTextTimesUint, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )


		sbSizerSignalSet.Add( setSizer1, 1, wx.EXPAND, 5 )

		self.m_staticline11 = wx.StaticLine( sbSizerSignalSet.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		sbSizerSignalSet.Add( self.m_staticline11, 0, wx.EXPAND |wx.ALL, 5 )

		gSizerButton = wx.GridSizer( 0, 2, 0, 0 )

		self.m_btnAddTestCase = wx.Button( sbSizerSignalSet.GetStaticBox(), wx.ID_ANY, u"添加测试条件", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizerButton.Add( self.m_btnAddTestCase, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		self.m_btnClearTestCase = wx.Button( sbSizerSignalSet.GetStaticBox(), wx.ID_ANY, u"清空测试条件", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizerButton.Add( self.m_btnClearTestCase, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		self.m_btnSaveTestCase = wx.Button( sbSizerSignalSet.GetStaticBox(), wx.ID_ANY, u"保存测试条件", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizerButton.Add( self.m_btnSaveTestCase, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		self.m_btnLoadTestCase = wx.Button( sbSizerSignalSet.GetStaticBox(), wx.ID_ANY, u"加载测试条件", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizerButton.Add( self.m_btnLoadTestCase, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


		sbSizerSignalSet.Add( gSizerButton, 0, wx.EXPAND, 5 )


		rightSetSizerMain.Add( sbSizerSignalSet, 1, wx.EXPAND, 5 )


		self.m_rightpanel.SetSizer( rightSetSizerMain )
		self.m_rightpanel.Layout()
		rightSetSizerMain.Fit( self.m_rightpanel )
		self.m_splitterOutter.SplitVertically( self.m_leftpanel, self.m_rightpanel, 530 )
		OutterSizer.Add( self.m_splitterOutter, 1, wx.EXPAND, 5 )


		self.SetSizer( OutterSizer )
		self.Layout()

		# Connect Events
		self.m_listTestCase.Bind( wx.EVT_LISTBOX_DCLICK, self.OnTestCaseDClick )
		self.m_btnSignalConnect.Bind( wx.EVT_BUTTON, self.OnButtonSignalConnectClick )
		self.m_btn_MiddleFlush.Bind( wx.EVT_BUTTON, self.OnButtonMiddleFlushClick )
		self.m_btn_MiddleConnect.Bind( wx.EVT_BUTTON, self.OnButtonMiddleConnectClick )
		self.m_btnClearResult.Bind( wx.EVT_BUTTON, self.OnButtonClearTestResultClick )
		self.m_btnStartTest.Bind( wx.EVT_BUTTON, self.OnButtonStartTestClick )
		self.m_btnStopTest.Bind( wx.EVT_BUTTON, self.OnButtonStopTestClick )
		self.m_btnOpenResultFolder.Bind( wx.EVT_BUTTON, self.OnButtonOpenResultFolderClick )
		self.m_ckBoxIsVariable.Bind( wx.EVT_CHECKBOX, self.OnCkVariableParamClick )
		self.m_radioHighVol.Bind( wx.EVT_RADIOBUTTON, self.OnRadioParamClick )
		self.m_radioLowVol.Bind( wx.EVT_RADIOBUTTON, self.OnRadioParamClick )
		self.m_radioRiseTime.Bind( wx.EVT_RADIOBUTTON, self.OnRadioParamClick )
		self.m_radioDeclineTime.Bind( wx.EVT_RADIOBUTTON, self.OnRadioParamClick )
		self.m_cbBoxRiseTimeUint.Bind( wx.EVT_COMBOBOX, self.OnTimeUintcbBoxChanged )
		self.m_cbBoxDeclineTimeUint.Bind( wx.EVT_COMBOBOX, self.OnTimeUintcbBoxChanged )
		self.m_btnAddTestCase.Bind( wx.EVT_BUTTON, self.OnButtonAddTestCaseClick )
		self.m_btnClearTestCase.Bind( wx.EVT_BUTTON, self.OnButtonClearTestCaseClick )
		self.m_btnSaveTestCase.Bind( wx.EVT_BUTTON, self.OnButtonSaveTestCaseClick )
		self.m_btnLoadTestCase.Bind( wx.EVT_BUTTON, self.OnButtonLoadTestCaseClick )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def OnTestCaseDClick( self, event ):
		event.Skip()

	def OnButtonSignalConnectClick( self, event ):
		event.Skip()

	def OnButtonMiddleFlushClick( self, event ):
		event.Skip()

	def OnButtonMiddleConnectClick( self, event ):
		event.Skip()

	def OnButtonClearTestResultClick( self, event ):
		event.Skip()

	def OnButtonStartTestClick( self, event ):
		event.Skip()

	def OnButtonStopTestClick( self, event ):
		event.Skip()

	def OnButtonOpenResultFolderClick( self, event ):
		event.Skip()

	def OnCkVariableParamClick( self, event ):
		event.Skip()

	def OnRadioParamClick( self, event ):
		event.Skip()




	def OnTimeUintcbBoxChanged( self, event ):
		event.Skip()


	def OnButtonAddTestCaseClick( self, event ):
		event.Skip()

	def OnButtonClearTestCaseClick( self, event ):
		event.Skip()

	def OnButtonSaveTestCaseClick( self, event ):
		event.Skip()

	def OnButtonLoadTestCaseClick( self, event ):
		event.Skip()

	def m_splitterOutterOnIdle( self, event ):
		self.m_splitterOutter.SetSashPosition( 530 )
		self.m_splitterOutter.Unbind( wx.EVT_IDLE )

	def m_splitterTestCaseAndComPortOnIdle( self, event ):
		self.m_splitterTestCaseAndComPort.SetSashPosition( 300 )
		self.m_splitterTestCaseAndComPort.Unbind( wx.EVT_IDLE )


