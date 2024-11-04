# OpenBMCLAPI BABY API 使用文档

## 概述
OpenBMCLAPI BABY API 是一个基于 Flask 的 API，主要用于管理和监控系统状态以及一些配置文件的更新。

## 基础路径
所有 API 的基础路径为 `http://<host>:5000`。

## 初始化
在启动服务器时，API 会读取密码文件 `password`，并初始化 `uapassword` 变量。如果文件未找到，`uapassword` 将为空。

## API 接口

### 1. 用户代理验证
- **方法**: `GET`
- **路由**: `/password?value=<new_user_agent>`
- **描述**: 更新用户代理检查密码并将其写入 `password` 文件。
- **请求示例**:
    ```
    GET /password?value=YourNewUserAgentPassword
    ```
- **响应**:
    - 成功: `{"message": "用户代理密码已更新并写入文件", "new_user_agent": "<new_user_agent>"}`
    - 失败: `{"message": "未提供新的用户代理密码值"}`

### 2. 更新 openbmclapiready
- **方法**: `POST`
- **路由**: `/openbmclapireadyadd`
- **请求体**: `{ "value": "<new_value>" }`
- **描述**: 更新 `openbmclapiready` 的值并写入注册表。
- **响应**:
    - 成功: `{"message": "值已更新", "openbmclapiready": "<new_value>"}`
    - 失败: `{"message": "未提供值"}`

### 3. 启动程序
- **方法**: `GET`
- **路由**: `/openbmclapistart`
- **描述**: 启动指定的可执行文件。
- **响应**:
    - 成功: `"程序已启动！"`
    - 失败: `{"error": "启动程序时出错: <error_message>"}`

### 4. 获取系统信息
- **方法**: `GET`
- **路由**: `/testbaby`
- **描述**: 获取计算机名、IP 地址、RAM 大小、最大网络速率等信息。
- **响应**:
    ```json
    {
        "hostname": "<hostname>",
        "ip_address": "<ip_address>",
        "ram_size": <ram_size>,
        "max_network_speed": <max_speed>,
        "openbmclapireadystatus": "<openbmclapiready>",
        "nginxstatus": <nginxstatus>,
        "aliststatus": <aliststatus>,
        "openbmclapistatus": "<openbmclapiready>"
    }
    ```

### 5. 获取 CPU 信息
- **方法**: `GET`
- **路由**: `/cpuinfo`
- **描述**: 获取当前的 CPU 使用率。
- **响应**:
    ```json
    {
        "cpu_usage": <cpu_usage>
    }
    ```

### 6. 获取网络信息
- **方法**: `GET`
- **路由**: `/networkinfo`
- **描述**: 获取当前的网络上传速率。
- **响应**:
    ```json
    {
        "upload_speed_mbps": <upload_speed>
    }
    ```

### 7. 启动 Alist
- **方法**: `GET`
- **路由**: `/openalist`
- **描述**: 启动指定的 Alist。
- **响应**:
    - 成功: `"程序已启动！"`
    - 失败: `{"error": "启动程序时出错: <error_message>"}`

### 8. 获取 Alist 状态
- **方法**: `GET`
- **路由**: `/aliststatus`
- **描述**: 获取 Alist 的启动状态。
- **响应**:
    - `alist状态: 已启动` 或 `alist状态: 未启动`

### 9. 更新 Nginx 配置
- **方法**: `POST`
- **路由**: `/nginxconf`
- **描述**: 上传新的 `nginx.conf` 配置文件。
- **请求为**：通过表单上传文件，字段名为 `file`。
- **响应**:
    - 成功: `{"message": "成功更新 nginx 配置文件。"}`
    - 失败: `{"error": "未提供 nginx.conf 文件。"}` 或 `{"error": "请上传名为 nginx.conf 的文件。"}`

### 10. 更新 .env 文件中的各项配置
- **更新 cluid**:
    - **方法**: `GET`
    - **路由**: `/update_cluid/<id>`
    - **描述**: 更新 `cluid` 值。
    - **响应**:
        ```json
        {
            "message": "cluid已更新",
            "new_cluid": "<id>"
        }
        ```

- **更新 secid**:
    - **方法**: `GET`
    - **路由**: `/update_secid/<secid>`
    - **描述**: 更新 `secid` 值。
    - **响应**:
        ```json
        {
            "message": "secid已更新",
            "new_secid": "<secid>"
        }
        ```

- **更新 port**:
    - **方法**: `GET`
    - **路由**: `/update_port/<port>`
    - **描述**: 更新 `port` 值。
    - **响应**:
        ```json
        {
            "message": "port已更新",
            "new_port": "<port>"
        }
        ```

### 11. 获取节点状态
- **方法**: `GET`
- **路由**: `/status`
- **描述**: 获取节点的启动状态。
- **响应**:
  - `节点状态: 未启动`
  - `节点状态: 已启动`
  - `节点状态: 未知`
### 12.注意的一些东西
- 请不要在生产环境中使用默认的123456密码，请使用更安全的密码。
- 在访问主机的时候（比如RDP这种）需要注意密码，请看以下的密码
- `user：OBABAdmin`
- `password：ADm8H%MdA`
- 默认密码在登录系统后可更改。

## 注意事项
- API 中的所有请求和响应都应根据实际情况进行验证和错误处理。
- 确保在生产环境中使用 SSL/TLS 来保护数据传输的安全。
