import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse

def get_wlan_params():
    # 发送GET请求，并允许自动重定向
    url = "http://www.msftconnecttest.com/redirect"
    response = requests.get(url, allow_redirects=True)

    # 获取最终响应的URL
    final_url = response.url

    # 解析URL并获取远程主机地址和端口号
    parsed_url = urlparse(final_url)
    remote_host = parsed_url.netloc

    # 提取URL中的参数信息
    query_params = dict(re.findall(r'[\?&]([^=]+)=([^&]*)', final_url))
    user_ip = query_params.get('userip')
    nas_ip = query_params.get('nasip')
    user_mac = query_params.get('user-mac')

    # 返回参数信息以及远程主机地址和端口号
    return {
        'user_ip': user_ip,
        'nas_ip': nas_ip,
        'user_mac': user_mac,
        'final_url': final_url,
        'remote_host': remote_host
    }