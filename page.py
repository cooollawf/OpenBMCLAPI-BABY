import sys
import subprocess
import socket
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QMessageBox, QPushButton

class SimpleWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 设置窗口样式
        self.setWindowTitle("OpenBMCLAPI宝")
        self.setFixedSize(800, 600)
        
        # 创建布局和输入框
        layout = QVBoxLayout()
        
        self.input_field = QLineEdit(self)
        self.input_field.setFixedSize(300, 100)
        self.input_field.setStyleSheet("background-color: white;")
        self.input_field.setPlaceholderText("请输入IP地址并回车")
        
        self.ip = self.load_ip_from_file()
        if self.ip:
            self.input_field.setText(self.ip)

        layout.addWidget(self.input_field)

        # 添加密码输入框
        self.password_field = QLineEdit(self)
        self.password_field.setEchoMode(QLineEdit.Password)
        self.password_field.setFixedSize(300, 100)
        self.password_field.setStyleSheet("background-color: white;")
        self.password_field.setPlaceholderText("请输入密码")
        layout.addWidget(self.password_field)

        # 添加执行curl的按钮
        self.curl_button = QPushButton("检查机器状态", self)
        self.curl_button.setFixedSize(100, 100)
        self.curl_button.clicked.connect(self.execute_curl)
        layout.addWidget(self.curl_button)

        # 添加查找设备按钮
        self.find_devices_button = QPushButton("查找设备", self)
        self.find_devices_button.setFixedSize(100, 100)
        self.find_devices_button.clicked.connect(self.find_devices)
        layout.addWidget(self.find_devices_button)

        self.setLayout(layout)

        # 绑定回车事件
        self.input_field.returnPressed.connect(self.write_to_file)

    def load_ip_from_file(self):
        """ 从文件中读取IP地址并返回 """
        try:
            with open('ip.txt', 'r') as file:
                return file.readline().strip()
        except Exception as e:
            QMessageBox.critical(self, "错误", f"读取文件时出现错误: {str(e)}")
            return None

    def write_to_file(self):
        ip_content = self.input_field.text()
        if ip_content:
            try:
                with open('ip.txt', 'w') as file:
                    file.write(ip_content + '\n')
                self.input_field.clear()
                QMessageBox.information(self, "成功", "IP地址已保存。")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"写入文件时出现错误: {str(e)}")
        else:
            QMessageBox.warning(self, "警告", "输入内容不能为空！")

    def execute_curl(self):
        """ 执行 curl 命令 """
        ip = self.input_field.text()
        password = self.password_field.text()

        if ip and password:
            try:
                command = f'curl -H "User-Agent: {password}" http://{ip}:5000/testbaby'
                result = subprocess.run(command, shell=True, capture_output=True, text=True)

                output_lines = result.stdout.strip().splitlines()
                formatted_output = ""

                for line in output_lines:
                    if "hostname" in line:
                        formatted_output += f"主机名: {line.split(': ')[1]}\n"
                    elif "ip_address" in line:
                        formatted_output += f"IP 地址: {line.split(': ')[1]}\n"
                    elif "ram_size" in line:
                        formatted_output += f"RAM 大小: {line.split(': ')[1]}\n"
                    elif "max_network_speed" in line:
                        formatted_output += f"最高速率: {line.split(': ')[1]}\n"
                    elif "openbmclapi ready" in line:
                        formatted_output += f"openbmclapi ready编号: {line.split(': ')[1]}\n"

                if formatted_output:
                    QMessageBox.information(self, "执行结果", formatted_output)
                else:
                    QMessageBox.warning(self, "执行结果", "未获得有效的返回内容。")
                    
            except Exception as e:
                QMessageBox.critical(self, "错误", f"执行 curl 命令时出现错误: {str(e)}")
        else:
            QMessageBox.warning(self, "警告", "IP地址和密码不能为空！")

    def find_devices(self):
        """ 查找局域网设备 """
        local_ip = socket.gethostbyname(socket.gethostname())
        base_ip = local_ip.rsplit('.', 1)[0]
        ip_addresses = [f"{base_ip}.{i}" for i in range(1, 255)]

        results = []
        password = self.password_field.text()
        for ip in ip_addresses:
            try:
                command = f'curl -H "User-Agent: {password}" http://{ip}:5000/testbaby'
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    results.append(ip)
            except Exception as e:
                continue

        if results:
            QMessageBox.information(self, "查找结果", f"发现设备：\n" + "\n".join(results))
        else:
            QMessageBox.warning(self, "查找结果", "没有找到设备。")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SimpleWindow()
    window.show()
    sys.exit(app.exec_())
