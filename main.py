from flask import Flask
import subprocess
import psutil
import time
import socket
import winreg
from flask import jsonify, request

openbmclapistatus = 0
aliststatus = 0
openbmclapiready = 'T00001'
nginxstatus = 0
uapassword = ''  # 初始化uapassword变量

print("OpenBMCLAPI BabySystemServer(BSS) is running...")
print("检查成功，等待请求...")
print("Waiting for requests...")

app = Flask(__name__)

last_bytes_sent = 0
last_time = time.time()

# 读取password文件内容并初始化uapassword变量
def init_uapassword_file():
    global uapassword
    try:
        with open('password', 'r') as f:
            uapassword = f.read().strip()  # 读取内容并去除首尾空白字符
        print(f'uapassword变量已初始化: {uapassword}')
    except FileNotFoundError:
        print('password文件未找到，uapassword将为空')
    except Exception as e:
        print(f'初始化uapassword时出错: {str(e)}')

def write_to_registry(value):
    # 写入注册表，该示例以 HKEY_CURRENT_USER 为例
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\OpenBMCLAPI", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "openbmclapiready", 0, winreg.REG_SZ, value)
        winreg.CloseKey(key)
    except Exception as e:
        print(f'写入注册表时出错: {str(e)}')

@app.before_request
def check_user_agent():
    # 检查请求的 User-Agent 是否与 uapassword 匹配
    if request.headers.get('User-Agent') != uapassword:
        return '拒绝访问：无效的用户代理', 403

@app.route('/openbmclapireadyadd', methods=['POST'])
def update_openbmclapiready():
    global openbmclapiready
    try:
        data = request.json
        new_value = data.get('value')
        if new_value:
            openbmclapiready = new_value
            write_to_registry(openbmclapiready)  # 写入注册表
            return jsonify({'message': '值已更新', 'openbmclapiready': openbmclapiready}), 200
        else:
            return jsonify({'message': '未提供值'}), 400
    except Exception as e:
        return f'更新 openbmclapiready 时出错: {str(e)}', 500
    
@app.route('/password', methods=['GET'])
def change_user_agent():
    try:
        new_user_agent = request.args.get('value')
        if new_user_agent:
            # 将新用户代理值写入到password文件中
            with open('password', 'w') as f:
                f.write(new_user_agent + '\n')
            # 重新初始化uapassword
            init_uapassword_file()
            return jsonify({'message': '用户代理已更新并写入文件', 'new_user_agent': new_user_agent}), 200
        else:
            return jsonify({'message': '未提供新的用户代理值'}), 400
    except Exception as e:
        return f'更新用户代理时出错: {str(e)}', 500

@app.route('/openbmclapistart', methods=['GET'])
def open_program():
    try:
        # 打开指定的可执行文件
        subprocess.Popen(['C:\\oba-node\\run.bat'], shell=True)
        global openbmclapistatus
        openbmclapistatus = 1
        return '程序已启动！', 200
    except Exception as e:
        return f'启动程序时出错: {str(e)}', 500

@app.route('/testbaby', methods=['GET'])
def test_baby():
    try:
        # 获取计算机名
        hostname = socket.gethostname()
        # 获取 IP 地址
        ip_address = socket.gethostbyname(hostname)
        # 获取 RAM 大小 (单位: GB)
        ram_size = round(psutil.virtual_memory().total / (1024 ** 3), 2)

        # 获取网卡最高速率
        max_speed = max((net.speed for net in psutil.net_if_stats().values()), default=0)

        return {
            'hostname': hostname,
            'ip_address': ip_address,
            'ram_size': ram_size,
            'max_network_speed': max_speed,
            'openbmclapireadystatus': openbmclapiready,
            'nginxstatus': nginxstatus,
            'aliststatus': aliststatus,
            'openbmclapistatus': openbmclapiready,
        }, 200

    except Exception as e:
        return f'启动babysysteminfo 时出错: {str(e)}', 500

@app.route('/status', methods=['GET'])
def get_status():
    try:
        if openbmclapistatus == 0:
            return '节点状态: 未启动', 200
        elif openbmclapistatus == 1:
            return '节点状态: 已启动', 200
        else:
            return '节点状态: 未知', 200
    except Exception as e:
        return f'检查节点状态时出错: {str(e)}', 500

@app.route('/cpuinfo', methods=['GET'])
def get_cpu_info():
    try:
        cpu_usage = psutil.cpu_percent(interval=1)
        return {'cpu_usage': cpu_usage}, 200
    except Exception as e:
        return f'获取 CPU 信息时出错: {str(e)}', 500    

@app.route('/networkinfo', methods=['GET'])
def get_network_info():
    try:
        # 获取当前的网络I/O状态
        net_io_initial = psutil.net_io_counters()
        time.sleep(1)  # 等待1秒以计算速率
        net_io_final = psutil.net_io_counters()

        # 计算上传速率 (字节每秒)
        bytes_sent = net_io_final.bytes_sent - net_io_initial.bytes_sent
        upload_speed_mbps = (bytes_sent * 8) / 1_000_000  # 转换为 Mbps

        return {'upload_speed_mbps': upload_speed_mbps}, 200
    except Exception as e:
        return f'获取网络信息时出错: {str(e)}', 500

@app.route('/openalist', methods=['GET'])
def open_alist():
    try:
        # 打开指定的可执行文件
        subprocess.Popen(['C:\\OpenBMCLAPI\\alist\\alist.bat'], shell=True)
        global aliststatus
        aliststatus = 1
        return '程序已启动！', 200
    except Exception as e:
        return f'启动程序时出错: {str(e)}', 500

@app.route('/aliststatus', methods=['GET'])
def test_alist():
    try:
        # 发送测试信息
        if aliststatus == 0:
            return 'alist状态: 未启动', 200
        elif aliststatus == 1:
            return 'alist状态: 已启动', 200
        else:
            return '节点状态: 未知', 200
    except Exception as e:
        return f'检查节点状态时出错: {str(e)}', 500

@app.route('/nginxconf', methods=['POST'])
def update_nginx_conf():
    try:
        # 检查是否有文件上传
        if 'file' not in request.files:
            return jsonify({'error': '未提供 nginx.conf 文件。'}), 400

        uploaded_file = request.files['file']

        # 确保文件名是 nginx.conf
        if uploaded_file.filename != 'nginx.conf':
            return jsonify({'error': '请上传名为 nginx.conf 的文件。'}), 400

        # 将内容写入 nginx.conf 文件
        with open('C:\\OpenBMCLAPI\\nginx\\conf\\nginx.conf', 'wb') as conf_file:
            conf_file.write(uploaded_file.read())
        
        return jsonify({'message': '成功更新 nginx 配置文件。'}), 200

    except Exception as e:
        return jsonify({'error': f'更新 nginx 配置文件时出错: {str(e)}'}), 500

import os

@app.route('/update_cluid/<id>', methods=['GET'])
def update_cluid(id):
    try:
        # 获取当前文件的目录
        current_directory = os.path.dirname(os.path.abspath(__file__))
        # 指定env文件的路径
        env_file_path = os.path.join(current_directory, 'OpenBMCLAPI', '.env')

        # 读取当前的env文件内容
        with open(env_file_path, 'r') as f:
            lines = f.readlines()

        # 找到并替换CLUSTER_ID的值
        for i, line in enumerate(lines):
            if line.startswith('CLUSTER_ID='):
                lines[i] = f'CLUSTER_ID={id}\n'  # 替换CLUSTER_ID后的值

        # 写回env文件
        with open(env_file_path, 'w') as f:
            f.writelines(lines)

        return jsonify({'message': 'CLUSTER_ID已更新', 'new_cluster_id': id}), 200
    except FileNotFoundError:
        return jsonify({'error': 'env文件未找到'}), 404
    except Exception as e:
        return jsonify({'error': f'更新CLUSTER_ID时出错: {str(e)}'}), 500

@app.route('/update_secid/<secid>', methods=['GET'])
def update_secid(secid):  # 修改函数名
    try:
        # 获取当前文件的目录
        current_directory = os.path.dirname(os.path.abspath(__file__))
        # 指定env文件的路径
        env_file_path = os.path.join(current_directory, 'OpenBMCLAPI', '.env')

        # 读取当前的env文件内容
        with open(env_file_path, 'r') as f:
            lines = f.readlines()

        # 找到并替换CLUSTER_SECRET的值
        for i, line in enumerate(lines):
            if line.startswith('CLUSTER_SECRET='):
                lines[i] = f'CLUSTER_SECRET={secid}\n'  # 替换CLUSTER_SECRET后的值

        # 写回env文件
        with open(env_file_path, 'w') as f:
            f.writelines(lines)

        return jsonify({'message': 'CLUSTER_SECRET已更新', 'new_cluster_secret': secid}), 200
    except FileNotFoundError:
        return jsonify({'error': 'env文件未找到'}), 404
    except Exception as e:
        return jsonify({'error': f'更新CLUSTER_SECRET时出错: {str(e)}'}), 500


@app.route('/update_port/<port>', methods=['GET'])
def update_port(port):  # 修改函数名
    try:
        # 获取当前文件的目录
        current_directory = os.path.dirname(os.path.abspath(__file__))
        # 指定env文件的路径
        env_file_path = os.path.join(current_directory, 'OpenBMCLAPI', '.env')

        # 读取当前的env文件内容
        with open(env_file_path, 'r') as f:
            lines = f.readlines()

        # 找到并替换CLUSTER_PORT的值
        for i, line in enumerate(lines):
            if line.startswith('CLUSTER_PORT='):
                lines[i] = f'CLUSTER_PORT={port}\n'  # 替换CLUSTER_PORT后的值

        # 写回env文件
        with open(env_file_path, 'w') as f:
            f.writelines(lines)

        return jsonify({'message': 'CLUSTER_PORT已更新', 'new_cluster_port': port}), 200
    except FileNotFoundError:
        return jsonify({'error': 'env文件未找到'}), 404
    except Exception as e:
        return jsonify({'error': f'更新CLUSTER_PORT时出错: {str(e)}'}), 500



if __name__ == '__main__':
    init_uapassword_file()  # 启动时初始化uapassword变量
    app.run(debug=True, host='0.0.0.0', port=5000)
