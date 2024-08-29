# ------- Litang Save The World! -------
#
# @Time    : 2023/6/26 22:03
# @Author  : Lynx
# @File    : emp_list.py
#
import json
from HRM_system import HRM_system
from SQL_controller import SQL_controller
from employee import *


class emp_list(list):
    id_format = None
    sys = None
    sql = None

    def __init__(self, system: HRM_system, sql: SQL_controller) -> None:
        # 构造函数
        super().__init__()
        self.sys = system
        self.sql = sql
        res = self.sql.sync()
        for row in res:
            emp = {
                'id': int(row[0]),
                'name': row[1],
                'sex': row[2],
                'address': row[3],
                'email': row[4],
                'sal': int(row[5]),
                'atte': int(row[6])
            }
            self.append(emp)

    def isEmpty(self):
        # 辅助函数：判断员工列表是否为空
        if not self:
            print('没有任何员工信息存在！')
            return True
        return False

    def getEmpId(self) -> int:
        # 辅助函数：获取员工编号
        id = self.sys.getMsg('员工编号', 0)
        while True:
            try:
                id = int(id)
                break
            except:
                self.sys.printInfo('员工编号不合法')
                msg = self.sys.getMsg('员工编号', 1)
                if msg[1] == 1:
                    raise Exception
                else:
                    id = msg[0]
        return id

    def getEmpName(self) -> str:
        # 辅助函数：获取员工姓名
        name = self.sys.getMsg('员工姓名', 0)
        while not nameJudge(name):
            self.sys.printInfo('员工姓名不合法')
            msg = self.sys.getMsg('员工姓名', 1)
            if msg[1] == 1:
                raise Exception
            else:
                name = msg[0]
        return name

    def getEmpSex(self) -> str:
        # 辅助函数：获取员工性别
        sex = self.sys.getMsg('员工性别', 0)
        while not sexJudge(sex):
            self.sys.printInfo('员工性别不合法')
            msg = self.sys.getMsg('员工性别', 1)
            if msg[1] == 1:
                raise Exception
            else:
                sex = msg[0]
        return sex

    def getEmpEmail(self) -> str:
        # 辅助函数：获取员工邮箱
        email = self.sys.getMsg('员工邮箱', 0)
        while not emailJudge(email):
            self.sys.printInfo('员工邮箱不合法')
            msg = self.sys.getMsg('员工邮箱', 1)
            if msg[1] == 1:
                raise Exception
            else:
                email = msg[0]
        return email

    def getEmpSal(self) -> int:
        # 辅助函数：获取员工工资
        sal = self.sys.getMsg('员工薪酬', 0)
        while True:
            try:
                sal = int(sal)
                break
            except:
                self.sys.printInfo('员工薪酬不合法')
                msg = self.sys.getMsg('员工薪酬', 1)
                if msg[1] == 1:
                    raise Exception
                else:
                    sal = msg[0]
        return sal

    def getEmpSetByJSON(self) -> list | None:
        # 辅助函数：通过JSON文件获取员工序列
        path = self.sys.getMsg('JSON文件路径（相对）', 0)
        while True:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    employees = json.load(f)
                return employees
            except Exception:
                self.sys.printInfo('无法打开或解析文件')
                msg = self.sys.getMsg('JSON文件路径（相对）', 1)
                if msg[1] == 1:
                    raise Exception
                else:
                    path = msg[0]

    def addByKeyboard(self) -> None:
        """
        add an employee by getting the information from user input

        note: we think the emp added from user must be a new emp, so
            we set the default atte to 0.
        :return: None
        """
        sig = True
        while sig:
            self.sys.printInfo('请输入员工信息')

            try:
                id = self.getEmpId()
                name = self.getEmpName()
                sex = self.getEmpSex()
                addr = self.sys.getMsg('员工住址', 0)
                email = self.getEmpEmail()
                sal = self.getEmpSal()
            except:
                return

            emp = empInit(id=id, name=name, sex=sex, address=addr, email=email, sal=sal)
            if any(emp['id'] == i['id'] for i in self):
                self.sys.printInfo('添加失败，新员工编号与系统中员工重复')
            else:
                try:
                    self.sql.create(emp)
                    self.append(emp)
                    self.sys.printInfo('添加成功！')
                except:
                    self.sys.printInfo('添加失败，请检查数据库连接')
                    return

            sig = self.sys.isLoop('添加员工信息')

    def addByJSON(self) -> None:
        # 通过JSON添加员工信息
        try:
            employeeSet = self.getEmpSetByJSON()
        except:
            return

        for employee in employeeSet:
            if any(employee.get('id') == emp['id'] for emp in self):
                self.sys.printInfo('添加失败，JSON文件中有员工编号与系统中员工重复')
                return

        for employee in employeeSet:
            id = employee.get('id')
            name = employee.get('name')
            sex = employee.get('sex')
            address = employee.get('address')
            email = employee.get('email')
            sal = employee.get('sal')
            atte = employee.get('atte')

            emp = empInit(id=id, name=name, sex=sex, address=address, email=email, sal=sal, atte=atte)
            try:
                self.sql.create(emp)
                self.append(emp)
            except:
                self.sys.printInfo('添加失败，请检查数据库连接')
                return

        self.sys.printInfo('导入成功！员工信息如下：')
        self.showAll()

    def showEmp(self, emp: dict) -> None:
        # 辅助函数：显示单个员工信息
        emp_msg = f'{emp["id"]}\t\t {emp["name"]}\t\t ' \
                  f'{emp["sex"]}\t\t {emp["address"]}\t\t ' \
                  f'{emp["email"]}\t\t {emp["sal"]}\t\t {emp["atte"]}'
        self.sys.printInfo(emp_msg)

    def showEmpDetail(self, emp: dict) -> None:
        # 辅助函数：显示单个员工详细信息
        self.sys.printInfo('-' * 25)
        self.sys.printInfo('编号：' + str(emp['id']))
        self.sys.printInfo('姓名：' + str(emp['name']))
        self.sys.printInfo('性别：' + str(emp['sex']))
        self.sys.printInfo('地址：' + str(emp['address']))
        self.sys.printInfo('邮箱：' + str(emp['email']))
        self.sys.printInfo('薪酬：' + str(emp['sal']))
        self.sys.printInfo('出勤情况：' + str(emp['atte']))
        self.sys.printInfo('-' * 25)

    def showConstraint(self):
        # 显示信息约束情况
        self.sys.printInfo('-' * 50)
        self.sys.printInfo('输入信息约束情况：')
        self.sys.printInfo('编号约束：需为整数，添加员工时需不与系统内员工编号重复')
        self.sys.printInfo('姓名约束：需为汉字或字母序列')
        self.sys.printInfo('性别约束：需为汉字‘男’或‘女’')
        self.sys.printInfo('地址约束：需为字符串')
        self.sys.printInfo('邮箱约束：需为以@和.为分隔符的多段英文字符序列，\n' + \
                           '\t\t其中@仅出现一次且不是最后一个分隔符，其他分隔符必须为.')
        self.sys.printInfo('薪酬约束：需为整数')
        self.sys.printInfo('-' * 50)

    def showAll(self) -> None:
        # 显示所有员工信息
        if self.isEmpty(): return

        self.sys.printInfo('*' * 46 + ' 员工列表 ' + '*' * 46 + '\n' + \
                           '-' * 100 + '\n' + \
                           '编号\t\t 姓名\t\t 性别\t\t 地址\t\t\t\t\t 邮箱\t\t\t\t 薪酬\t\t 出勤情况\n' + \
                           '-' * 100)
        sorted_employees = sorted(self, key=lambda emp: emp['id'])

        for emp in sorted_employees:
            self.showEmp(emp)

        self.sys.printInfo('-' * 100)

    def findEmp(self, key, value) -> dict | None:
        '''
        Find the employee from the emp_list by the key and the value received
        :param key: Employee attributes
        :param value: The corresponding value of this attribute
        :return: None
        '''
        for i in self:
            if i[key] == value:
                return i
        return None

    def updateEmp(self) -> None:
        # 修改员工信息（通过编号）
        if self.isEmpty(): return
        try:
            id = self.getEmpId()
        except:
            return

        emp = self.findEmp('id', id)
        if emp == None:
            self.sys.printInfo('没有该编号的员工信息存在！')
            return

        self.sys.printInfo('要修改的员工信息为：')
        self.showEmpDetail(emp)

        self.sys.printInfo('输入新的员工信息')
        try:
            addr = self.sys.getMsg('员工地址', 0)
            email = self.getEmpEmail()
            sal = self.getEmpSal()
        except:
            return

        emp_copy = emp.copy()

        emp_copy['address'] = addr
        emp_copy['email'] = email
        emp_copy['sal'] = sal
        try:
            self.sql.update(emp_copy)
        except:
            self.sys.printInfo('更新失败！请检查数据库连接')
            return

        emp['address'] = addr
        emp['email'] = email
        emp['sal'] = sal

        self.sys.printInfo('更新成功！新的员工信息为：')
        self.showEmpDetail(emp)

    def deleteEmp(self) -> None:
        # 删除员工（通过编号）
        if self.isEmpty(): return
        try:
            id = self.getEmpId()
        except:
            return
        emp = self.findEmp('id', id)
        if emp == None:
            self.sys.printInfo('没有该编号的员工信息存在！')
            return

        self.sys.printInfo('要删除的员工信息为：')
        self.showEmpDetail(emp)
        try:
            self.sql.delete(emp)
            self.remove(emp)
            self.sys.printInfo('删除成功！')
        except:
            self.sys.printInfo('删除失败！请检查数据库连接')
            return

    def searchEmp(self) -> None:
        # 查找员工
        if self.isEmpty(): return
        mode = self.sys.getMsg('查找模式（编号/姓名）', 0)
        if mode == '姓名':
            self.searchEmpByName()
        elif mode == '编号':
            self.searchEmpById()
        else:
            self.sys.printInfo('输入内容有误，将按照默认模式（编号）查找：')
            self.searchEmpById()

    def searchEmpById(self) -> None:
        # 通过编号查找员工
        try:
            id = self.getEmpId()
        except:
            return

        emp = self.findEmp('id', id)
        if emp == None:
            self.sys.printInfo('没有该编号的员工信息存在！')
            return

        self.sys.printInfo('要查找的员工信息为：')
        self.showEmpDetail(emp)

    def searchEmpByName(self) -> None:
        # 通过姓名查找员工
        try:
            name = self.getEmpName()
        except:
            return

        emp = self.findEmp('name', name)
        if emp == None:
            self.sys.printInfo('没有该姓名的员工信息存在！')
            return

        self.sys.printInfo('要查找的员工信息为：')
        self.showEmpDetail(emp)

    def importEmpSetToJSON(self) -> None:
        # 导出员工列表到JSON文件
        path = self.sys.getMsg('导出路径', 0)
        while True:
            try:
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(self, f, indent=4)
                self.sys.printInfo('导出成功！')
                return
            except:
                self.sys.printInfo('导出失败，请检查员工列表信息和导出路径')
                msg = self.sys.getMsg('导出路径', 1)
                if msg[1] == 1:
                    return
                else:
                    path = msg[0]

    def signIn(self) -> None:
        # 员工签到
        if self.isEmpty(): return
        try:
            id = self.getEmpId()
        except:
            return

        emp = self.findEmp('id', id)
        if emp == None:
            self.sys.printInfo('没有该编号的员工存在！')
            return

        emp_copy = emp.copy()
        emp_copy['atte'] += 1
        try:
            self.sql.update(emp_copy)  # 使用副本进行更新
        except:
            self.sys.printInfo('更新失败！请检查数据库连接')
            return

        emp['atte'] += 1
        self.sys.printInfo('签到成功！该员工目前的出勤次数为：' + str(emp['atte']))

    def mainLoop(self) -> None:
        # 主循环，提供分支控制逻辑
        instSet = '=====员工信息管理系统=====\n' + \
                  '指令编号如下：\n' + \
                  '1 -- 添加员工\n' + \
                  '2 -- 查找员工\n' + \
                  '3 -- 修改员工信息\n' + \
                  '4 -- 删除员工\n' + \
                  '5 -- 显示所有员工信息\n' + \
                  '6 -- 从JSON文件导入员工信息\n' + \
                  '7 -- 导出员工列表到JSON文件\n' + \
                  '8 -- 员工签到\n' + \
                  '9 -- 查看输入信息约束\n' + \
                  '======================='
        cnt = 1
        while True:
            if cnt == 1:
                self.sys.printInfo(instSet)
            msg = self.sys.getMsg('指令编号', 1)
            if msg[1] == 1:
                return
            elif msg[0] in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
                if msg[0] == '1':
                    self.addByKeyboard()
                elif msg[0] == '2':
                    self.searchEmp()
                elif msg[0] == '3':
                    self.updateEmp()
                elif msg[0] == '4':
                    self.deleteEmp()
                elif msg[0] == '5':
                    self.showAll()
                elif msg[0] == '6':
                    self.addByJSON()
                elif msg[0] == '7':
                    self.importEmpSetToJSON()
                elif msg[0] == '8':
                    self.signIn()
                elif msg[0] == '9':
                    self.showConstraint()
                cnt = 1
            else:
                if cnt == 5:
                    return
                self.sys.printInfo('指令非法，请重新输入！(' + str(cnt) + \
                                   '/5)')
                cnt += 1
