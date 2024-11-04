import socket
import requests
import threading

# 用于存储每个 IP 的状态信息
response_data = {}
lock = threading.Lock()  # 创建一个锁
print("开始扫描局域网内的OpenBMCLAPI宝设备")

# 扫描局域网内的设备
def scan_local_network():
    local_ip = socket.gethostbyname(socket.gethostname())
    base_ip = local_ip.rsplit('.', 1)[0]  # 获取前3段IP地址
    return [f"{base_ip}.{i}" for i in range(1, 255)] + ["127.0.0.1"]  # 添加 localhost

# 对IP发送一次GET请求
def send_get_request(ip, user_agent):
    url = f"http://{ip}:5000/testbaby"  # 假设本地服务也有此路由
    headers = {'User-Agent': user_agent}  # 将用户输入的User-Agent放入请求头
    try:
        response = requests.get(url, headers=headers, timeout=1)  # 带上headers
        response.raise_for_status()  # 检查响应状态
        data = response.json()  # 假设返回的是 JSON 格式内容

        with lock:  # 使用锁确保线程安全
            response_data[ip] = data

    except requests.Timeout:
        print(f"请求超时: {ip}")
    except requests.RequestException as e:
        print(f"请求失败 {ip}: {str(e)}")

def main():
    user_agent = input("请输入机器上的初始密码，如果你的机子方案没有被OpenBMCLAPI宝审核，就输入123456为密码，如果你是已经初始化完成就输入你现在的密码: ")  # 获取用户输入的User-Agent
    ip_addresses = scan_local_network()

    # 使用线程来并发发送请求
    threads = [threading.Thread(target=send_get_request, args=(ip, user_agent)) for ip in ip_addresses]
    
    for thread in threads:
        thread.start()

    # 等待所有线程完成
    for thread in threads:
        thread.join()

    # 打印成功访问的 IP 的变量
    for ip, data in response_data.items():
        hostname = data.get('hostname', '未知')
        ip_address = data.get('ip_address', '未知')
        ram_size = data.get('ram_size', '未知')
        max_network_speed = data.get('max_network_speed', '未知')
        openbmclapistatus = data.get('openbmclapiready', '未知')
        aliststatus = data.get('aliststatus', '未知')
        nginxstatus = data.get('nginxstatus', '未知')
        openbmclapistatus = data.get('openbmclapistatus', '未知')  # 获取 openbmclapistatus

        print("OpenBMCLAPI宝 设备信息:")
        print(f"主机名: {hostname}")
        print(f"IP 地址: {ip_address}") 
        print(f"RAM 大小: {ram_size}") 
        print(f"最高速率: {max_network_speed}") 
        print(f"openbmclapi ready编号: {openbmclapistatus}")

        # 检查 aliststatus 的值
        if aliststatus == 0:
            print("alist状态：未启动")
        elif aliststatus == 1:
            print("alist状态：启动成功")   
        if nginxstatus == 0:
            print("nginx状态：未启动")
        elif nginxstatus == 1:
            print("nginx状态：启动成功") 
        if openbmclapistatus == 0:
            print("OpenBMCLAPI状态：未启动")
        elif openbmclapistatus == 1:
            print("OpenBMCLAPI状态：启动成功")          

if __name__ == "__main__":
    main()
