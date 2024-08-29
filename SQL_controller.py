# ------- Litang Save The World! -------
#
# @Time    : 2023/6/27 21:25
# @Author  : Lynx
# @File    : SQL_controller.py
#

import pymysql
import yaml

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

class SQL_controller:
    connection = None
    def __init__(self):
        self.connection = pymysql.connect(**config)
        self.create_table_if_not_exists()

    def create_table_if_not_exists(self):
        try:
            with self.connection.cursor() as cursor:
                # 检查表是否存在，如果不存在则创建
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS employee (
                        id INT PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        sex VARCHAR(10),
                        address VARCHAR(255),
                        email VARCHAR(255),
                        sal INT CHECK (sal > 0),
                        atte INT CHECK (atte > 0)
                    );
                """)
            self.connection.commit()
        except:
            self.connection.rollback()
            raise Exception

    def create(self, emp:dict) -> None:
        try:
            with self.connection.cursor() as cursor:
                sql = "INSERT INTO employee (id, name, sex, address, email, sal, atte) " \
                      "VALUES (%s, %s, %s, %s, %s, %s, %s)"

                cursor.execute(sql, (
                emp['id'], emp['name'], emp['sex'], emp['address'], emp['email'], emp['sal'], emp['atte']))

            self.connection.commit()
        except:
            self.connection.rollback()
            raise Exception

    def update(self, emp:dict) -> None:
        try:
            with self.connection.cursor() as cursor:
                sql = "UPDATE employee SET address = %s, email = %s, sal = %s WHERE id = %s"
                cursor.execute(sql, (emp['address'], emp['email'], emp['sal'], emp['id']))

            self.connection.commit()
        except:
            self.connection.rollback()
            raise Exception

    def delete(self, emp:dict) -> None:
        try:
            with self.connection.cursor() as cursor:
                sql = "DELETE FROM employee WHERE id = %s"

                cursor.execute(sql, emp['id'])
            self.connection.commit()
        except:
            self.connection.rollback()
            raise Exception

    def sync(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM employee")

                result = cursor.fetchall()
                return result
        except:
            self.connection.rollback()
            raise Exception

if __name__ == '__main__':
    print(config)
  #   sql = SQL_controller()
  #   sql.create({
  #   "id": 48,
  #   "name": "孙秀兰",
  #   "sex": "男",
  #   "address": "西藏自治区 昌都地区 贡觉县",
  #   "email": "w.kgspbp@zsllit.nu",
  #   "sal": 4600,
  #   "atte": 55
  # })
