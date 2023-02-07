class SignalCMD:
    Beep = ':SYSTem: BEEPer:IMMediate'
    Output1On = ':OUTPUT1 ON'
    Output1Off = ':OUTPUT1 OFF'

    @staticmethod
    def GetOUTPUTCmd(num: int, status: bool = True) -> str:
        """
        获取信号发生器输出命令
        :param status: True: ON , False: OFF
        :param num: 端口1or2
        :return: 输出cmd
        """
        if status:
            temp = 'ON'
        else:
            temp = 'OFF'
        cmd = ':OUTPUT%s %s' % (str(num), temp)
        return cmd