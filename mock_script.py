# ------- Litang Save The World! -------
#
# @Time    : 2023/6/27 17:47
# @Author  : Lynx
# @File    : mock_script.py
#
import requests
import json

if __name__ == '__main__':
    url = "https://mock.apifox.cn/m1/2932626-0-default/getEmp"
    output_file = input('输入保存地址：')
    num_requests = int(input('输入获取次数：'))

    employees = []

    for _ in range(num_requests):
        response = requests.get(url)
        if response.status_code == 200:
            employee = response.json()
            employees.append(employee)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(employees, f, indent=4)

    print("数据已成功写入文件：", output_file)