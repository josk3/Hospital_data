import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
import pandas as pd
import time
import random
import re
import os
from data import Properties_map, hosType_map
# 医院名称、医院所在省、医院所在市（区）、医院属性（公立、私立）、医院等级、医院类型（综合、专科、研究所.....）、医院详细地址、床位数（如有）
# 医院名称: 北京清华长庚医院, 省: 北京, 市: 昌平区, 医院属性: 公立医院, 等级: 三级丙等, 类型: 综合医院, 详细住址: 北京市昌平区立汤路168号, 床位: 1000

# 基础 URL
base_url = "https://y.dxy.cn/hospital"

# 请求头，模拟浏览器请求
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

# 医院详情: 获取地址 + 床位
def hospital_grade_son(hospital, session):
    hospital_link_element = hospital.select_one("a")
    if hospital_link_element is not None:
        hospital_link = hospital_link_element["href"]

        # 解析URL获取医院ID
        parsed_url = urlparse(hospital_link)
        hospital_id = parsed_url.path.split("/")[-1]  # 直接从路径中提取ID

        # 跳转医院url
        url2 = f"{base_url}/{hospital_id}/detail"
        response2 = session.get(url2, headers=headers)
        # 使用 BeautifulSoup 解析页面
        soup = BeautifulSoup(response2.text, "html.parser")

        # 详细住址
        address_tag = soup.select_one('.pc-hospital-detail div:nth-child(6) .block-body-single-content')
        address = address_tag.text.strip() if address_tag else "N/A"
        address = address.rsplit(" ", 1)[-1]
        # 床位
        bed_tag = soup.select_one(
            '.pc-hospital-detail div:nth-child(7) div:nth-child(2) .block-body-single-content')
        bed = bed_tag.text.strip() if bed_tag else "N/A"
        bed_nums = re.findall(r'\d+', bed)
        bed_num = int(bed_nums[0]) if bed_nums else 0
    else:
        address = "该医院未收录"
        bed_num = "该医院未收录"
        print("该医院未收录")
    return address, bed_num

# 主页面
def hospital_grade_main(grade_url, grade_name, location_url, location_name, sum):
    hospital_data = []
    # 页码控制
    page = 1
    cur_sum = 0
    session = requests.Session()
    while True:
        # 拼接分页 URL
        url = f"{base_url}?page={page}&grade={grade_url}&location={location_url}"
        response = session.get(url, headers=headers)

        if response.status_code != 200:
            print("请求失败，状态码:", response.status_code)
            break

        # 使用 BeautifulSoup 解析页面
        soup = BeautifulSoup(response.text, "html.parser")

        # 假设每页包含医院卡片的类名为 .hospital-card
        hospitals = soup.select(".main-listsbox .table .tbody .tr")  # 假设每个医院的卡片有一个 .hospital-card 的类名

        print('hospitals', hospitals)
        # 如果找不到医院数据，说明已到最后一页，结束循环
        if not hospitals:
            print("所有页面均已获取完毕。")
            break

        cnt = 0
        # 遍历并提取信息
        for hospital in hospitals:
            # if cnt == 2:
            #     break
            # 假设医院名称在 .hospital-name 类中，地区在 .hospital-region 类中
            name = hospital.select_one(".hospital-title").text.strip() if hospital.select_one(
                ".hospital-title") else "N/A"
            # 地区
            region = hospital.select_one(
                ".main-listsbox .table .tbody .tr .td:nth-child(2)").text.strip() if hospital.select_one(
                ".main-listsbox .table .tbody .tr .td:nth-child(2)") else "N/A"

            # 省
            province = region.split('·')[0]

            # 市
            city = region.split('·')[1]

            # 医院属性（公立）
            Properties = hospital.select_one(
                ".main-listsbox .table .tbody .tr .td:nth-child(3)").text.strip() if hospital.select_one(
                ".main-listsbox .table .tbody .tr .td:nth-child(3)") else "N/A"

            # 等级（三甲。。。）
            grade = hospital.select_one(
                ".main-listsbox .table .tbody .tr .td:nth-child(5)").text.strip() if hospital.select_one(
                ".main-listsbox .table .tbody .tr .td:nth-child(5)") else "N/A"

            # 类型（综合医院）
            hosType = hospital.select_one(
                ".main-listsbox .table .tbody .tr .td:nth-child(4)").text.strip() if hospital.select_one(
                ".main-listsbox .table .tbody .tr .td:nth-child(4)") else "N/A"


            # 子页面
            address, bed_num = hospital_grade_son(hospital, session)

            hospital_data.append({
                "医院名称": name,
                "省": province,
                "市": city,
                "医院属性": Properties_map.get(Properties, Properties),
                "等级": grade,
                "类型": hosType_map.get(hosType, hosType),
                "详细住址": address,
                "床位": bed_num
            })

            cnt = cnt + 1
            delay = random.uniform(1.2, 2.5)
            print(f"医院名称: {name}, 省: {province}, 市: {city}, 医院属性: {Properties_map.get(Properties, Properties)}, 等级: {grade}, 类型: {hosType_map.get(hosType, hosType)}, 详细住址: {address}, 床位: {bed_num}")
            print(f"延迟{delay}s, 当前在第{page}页, 第{cnt}个医院")
            # 设置延迟，避免请求过于频繁
            time.sleep(delay)  # 延迟 2 秒
            cur_sum = cur_sum + 1
        # 增加页码，继续爬取下一页
        delay = random.uniform(1, 3)
        print(f"第{page}页，延迟{delay}s")
        page += 1
        # 设置延迟，避免请求过于频繁
        time.sleep(delay)  # 延迟 2 秒

    # 指定保存目录
    save_dir = f'{location_name}'

    # 确保目录存在，如果不存在则创建
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # 构建文件名
    file_name = f"{location_name}-{grade_name}.xlsx"

    # 构建完整的文件路径
    full_path = os.path.join(save_dir, file_name)
    df = pd.DataFrame(hospital_data)
    df.to_excel(full_path, index=False, engine="openpyxl")
    print(f"数据已成功存储到 {location_name}-{grade_name}.xlsx 中")
    return sum + cur_sum