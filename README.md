# OpenBMCLAPI-BABY
## 简介
- OpenBMCLAPI-BABY是OpenBMCLAPI的垃圾机子专门部署版（类似网心云的“垃圾机”，但是安装系统需要自己手动安装），它是OpenBMCLAPI的改版，适用于小型服务器。
## 特点
- 使用Python写后端（
- 配置更简单（虽然请求软件没写完）
## 安装
1. 安装Python3.11或以上版本
2. 安装依赖包：
- `pip install -r requirements.txt`
3. 启动服务：
- python main.py`
4.curl测试：
-`curl http://自己机子ip地址:5000/testbaby`
5.按照api教程操作，根目录下的API.md文件有详细的API使用方法。
## 特殊的安装方法
- 由于OpenBMCLAPI-BABY的安装只是在你的机子上安装了后端，其他的操作都需要你自己手动操作，所以我们提供了一些ghost镜像，可以兼容小主机/nas等特殊客户机的安装。
- 下载ghost镜像：https://github.com/cooollawf/OpenBMCLAPI-BABY/releases/tag/v1.0.0（目前无镜像）
- 解压ghost镜像：`tar -zxvf ghost-v1.0.0.tar.gz`