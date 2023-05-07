import os
import json
import shutil
import time
import subprocess

config_path = os.path.join(os.path.dirname(__file__), "config.json")

# 检测config.json是否存在，不存在则新建config字典
if not os.path.exists(config_path):
    print("未检测到配置文件！正在重新创建...")
    config = {}
else:
    # 如果配置文件存在，提示用户读取并显示手机号和密码
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    if config.get("mobile") and config.get("password"):
        print("检测到已保存的手机号和密码：")
        print(f"手机号：{config['mobile']}")
        print(f"密码：{config['password']}")

        while True:
            modify = input("是否需要修改手机号和密码？(Y/N)：")
            if modify.lower() == "y":
                # 清空config中已保存的手机号和密码的值，方便后面的修改操作
                config["mobile"] = None
                config["password"] = None
                break
            elif modify.lower() == "n":
                break
            else:
                print("无效的输入，请输入Y或N来选择。")

# 如果不需要修改，继续运行主程序
if config.get("mobile") and config.get("password"):
    print("手机号和密码验证通过，正在运行主程序...")
else:
    # 如果需要修改手机或密码，则要求用户重新输入并保存
    if not config.get("mobile"):
        phone = input("请输入用于认证的手机号码：")
        config["mobile"] = phone

    if not config.get("password"):
        password = input("请输入用于认证网页的密码：")
        config["password"] = password
    
    # 将config写入config.json
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=4)

    print("手机号和密码已保存，正在运行主程序...")

subprocess.call("启动.exe", shell=True)