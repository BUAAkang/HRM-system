# ------- Litang Save The World! -------
#
# @Time    : 2023/6/26 22:00
# @Author  : Lynx
# @File    : HRM_system.py
#
from typing import Tuple


class HRM_system:
    # 交互控制台类，直接与用户进行交互，并将信息传至emp_list管理类
    def printInfo(self, info:str) -> None:
        print(info)

    def getMsg(self, hint:str, mode:int) -> str | tuple[None, int] | tuple[str, int]:
        '''
        While get the mode '1', we think that the system step into one specific module.
        When the input value is always illegal, the program will fall into a dead cycle.
        So we support a method to skip this cycle, the concrete implement is to create a quit
        listener, and return some specific value when listener response. That why this function
        is created.
        '''
        if mode == 0:
            return input('请输入' + hint + '：')
        else:
            msg = input('请输入' + hint + '，或输入‘Q’退出：')
            if msg == 'Q':
                return None, 1
            else: return msg, 0

    def isLoop(self, msg:str) -> bool:
        '''
        In some condition, the user can add some information repeatedly. So we set a signal to
        skip out of the loop. That why this function is created.
        '''
        sig = input('是否继续' + msg + '？[y/n]')
        if sig.lower() != 'y':
            return False
        return True

    def start(self) -> None:
        self.printInfo('欢迎使用员工信息管理系统！')

    def close(self) -> None:
        self.printInfo('感谢使用员工信息系统，再见！')

