import requests
from bs4 import BeautifulSoup

# 正确的URL
url = "https://y.dxy.cn/hospital/4"

# 设置请求头，模拟浏览器访问
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

try:
    session = requests.Session()
    # 发送GET请求
    response = session.get(url, headers=headers)

    # 检查请求是否成功
    if response.status_code == 200:
        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(response.text, 'html.parser')


        address_tag = soup.select_one('.pc-hospital-detail div:nth-child(6) .block-body-single-content')
        address = address_tag.text.strip() if address_tag else "N/A"

        # 打印医院名称和地址
        print("医院地址:", address)
    else:
        print("请求失败，状态码:", response.status_code)

except requests.exceptions.RequestException as e:
    # 打印异常信息
    print("请求过程中发生错误：", e)