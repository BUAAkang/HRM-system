# ------- Litang Save The World! -------
#
# @Time    : 2023/6/26 22:13
# @Author  : Lynx
# @File    : employee.py
#
import re

def empInit(id:int, name:str, sex:str, address:str, email:str, sal:int, atte:int = 0):
    """
    receive some params and return a dict.

    :param id: 编号
    :param name: 姓名
    :param sex: 性别
    :param address: 地址
    :param email: 邮箱
    :param sal: 薪酬（为整数）
    :param atte: 出勤情况（以次计）
    :return: emp: dict类型
    """
    return dict(id=id, name=name, sex=sex, address=address, email=email, atte=atte, sal=sal)

def nameJudge(name:str) -> bool:
    pattern = '^[a-zA-Z\u4e00-\u9fa5]+$'
    if re.match(pattern, name) == None:
        return False
    return True

def sexJudge(sex:str) -> bool:
    if sex == '男' or sex == '女':
        return True
    return False

def emailJudge(email) -> bool:
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(pattern, email) == None:
        return False
    return True