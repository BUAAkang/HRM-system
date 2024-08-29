# ------- Litang Save The World! -------
#
# @Time    : 2023/6/27 17:42
# @Author  : Lynx
# @File    : test.py
#
import unittest
from SQL_controller import SQL_controller

class TestSQLController(unittest.TestCase):
    def setUp(self):
        self.controller = SQL_controller

    def test_connection(self):
        # 测试数据库连接是否成功
        self.assertIsNotNone(self.controller.connection, "数据库连接失败")

    def tearDown(self):
        # 测试完成后关闭数据库连接
        if self.controller.connection:
            self.controller.connection.close()

if __name__ == '__main__':
    unittest.main()