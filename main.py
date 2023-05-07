from modules.get_info import get_wlan_params
import json
import requests    
import time
import codecs
import subprocess

# 读取配置文件
try:
    with codecs.open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print('找不到配置文件')
    exit()

def post_request():
    params = get_wlan_params()

    url = f"http://{params['remote_host']}/hw/internal_auth"  
    data = {
        "mobile": config['mobile'],
        "mobile_english": config['mobile'],
        "password": config['password'],
        "password_english": config['password'],
        "auth_type": "account",
        "enterprise_id": "51",
        "enterprise_url": "HBHUAWEI",
        "site_id": "4662",
        "client_mac": "",
        "nas_ip": "",
        "wlanacname": None,
        "user_ip": "",
        "3rd_ip": None,
        "ap_mac": None,
        "vlan": "11-11-11-11-11-11",
        "ssid": None,
        "vlan_id": None,
        "ip": None,
        "ac_ip": None,
        "from": None,
        "sn": None,
        "gw_id": None,
        "gw_address": None,
        "gw_port": None,
        "url": None,
        "language_tag": "0"
    }

    header = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Length": "",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Host": "",
        "Origin": "",
        "Referer": "",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.68",
        "X-Requested-With": "XMLHttpRequest"
    }

    json_data = json.dumps(data) # 将字典转换成JSON格式
    content_length = len(json_data)

    # 添加各种日志
    print("开始登录")
    data['user_ip'] = params['user_ip']
    data['nas_ip'] = params['nas_ip']
    data['client_mac'] = params['user_mac']
    header['Host'] = params['remote_host']
    header['Origin'] = f"http://{params['remote_host']}"
    header['Referer'] = f"http://{params['remote_host']}/hw/HBHUAWEI/login?apmac={data['client_mac']}&userip={data['user_ip']}&nasip={data['nas_ip']}&user-mac={params['user_mac']}"
    header['Content-Length'] = str(content_length)

    # 发送请求并记录时间
    start_time = time.time()
    try:
        response = requests.post(url, data, headers=header)
        status_code = response.status_code
    except requests.exceptions.Timeout:
        # 发送请求超时
        print('请求 {} 超时'.format(url))
        exit()
    except requests.exceptions.RequestException as e:
        # 请求发生了其他异常
        print('请求 {} 发生了异常：{}'.format(url, e))
        exit()

    end_time = time.time()

    # 添加响应时间信息
    print("请求 {} 耗时 {:.2f} 秒，状态码 {}".format(url, end_time-start_time, response.status_code))


# 设置定时器，实时监测网络状态
def check_internet():
    url = "https://www.baidu.com"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return True
        else:
            return False
    except:
        return False

while True:
    if check_internet():
        print("检测到网络连接正常，请勿关闭本窗口，5s后重新检测...")
        time.sleep(5)    
    else:
        print("网络连接异常，正在重新连接...")
        post_request()
        time.sleep(5)