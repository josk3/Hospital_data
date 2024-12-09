import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
import pandas as pd
import time
import random
import re
import os
from hospital_grade_main import hospital_grade_son
from data import Properties_map, hosType_map

def with_file(hospital_data):
    df = pd.DataFrame(hospital_data)
    # 定义文件名
    file_name = "data_all.xlsx"

    # 追加数据到已有的 Excel 文件中
    try:
        # 加载现有的工作簿
        with pd.ExcelWriter(file_name, mode="a", engine="openpyxl", if_sheet_exists="overlay") as writer:
            # 将数据写入工作簿的末尾，指定sheet_name
            df.to_excel(writer, index=False, sheet_name="Sheet1", header=False,
                        startrow=writer.sheets["Sheet1"].max_row)
        print(f"数据已成功追加到 {file_name} 中")
    except FileNotFoundError:
        # 如果文件不存在，创建新文件
        df.to_excel(file_name, index=False, engine="openpyxl")
        print(f"数据已成功存储到新文件 {file_name} 中")

base_url = "https://y.dxy.cn/hospital"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

# 页码控制
page = 3
session = requests.Session()
s = time.time()
while True:
    hospital_data = []

    # 拼接分页 URL
    url = f"{base_url}?page={page}"
    response = session.get(url, headers=headers)

    if response.status_code != 200:
        print("请求失败，状态码:", response.status_code)
        break

    # 使用 BeautifulSoup 解析页面
    soup = BeautifulSoup(response.text, "html.parser")

    # 假设每页包含医院卡片的类名为 .hospital-card
    hospitals = soup.select(".main-listsbox .table .tbody .tr")  # 假设每个医院的卡片有一个 .hospital-card 的类名

    # 如果找不到医院数据，说明已到最后一页，结束循环
    if not hospitals:
        print("所有页面均已获取完毕。")
        break

    cnt = 0
    # 遍历并提取信息
    for hospital in hospitals:
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
    # 增加页码，继续爬取下一页
    delay = random.uniform(1, 2.5)
    print(f"第{page}页，延迟{delay}s")
    page += 1

    with_file(hospital_data)

    # 设置延迟，避免请求过于频繁
    time.sleep(delay)  # 延迟 2 秒

# df = pd.DataFrame(hospital_data)
# df.to_excel("data_all.xlsx", index=False, engine="openpyxl")
# print(f"数据已成功存储到 data_all.xlsx 中")
