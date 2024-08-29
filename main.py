# ------- Litang Save The World! -------
#
# @Time    : 2023/6/27 16:35
# @Author  : Lynx
# @File    : main.py
#
from HRM_system import HRM_system
from SQL_controller import SQL_controller
from emp_list import emp_list

if __name__ == '__main__':
    sql = SQL_controller()
    system = HRM_system()
    system.start()
    list = emp_list(system, sql)
    list.mainLoop()
    system.close()
