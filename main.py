import time
import random
from hospital_grade_main import hospital_grade_main
from data import grade, locations


def hospital_grade_main_call1(grade_url, grade_name, location_url, location_name, sum):
    print(f"开始爬取{grade_name}的数据")
    return hospital_grade_main(grade_url, grade_name, location_url, location_name, sum)

def hospital_grade_main_call2(grade_url, grade_name, location_url, location_name, sum):
    print(f"开始爬取{grade_name}的数据")
    delay = random.uniform(1, 3)
    print(f"延迟时间：{delay}s")
    time.sleep(delay)
    return hospital_grade_main(grade_url, grade_name, location_url, location_name, sum)


for location in locations: # 每一个省份（北京、上海）
    s = time.time()
    sum = 0
    for index in locations[location]['grade']: # 每一个等级（三甲）
        if index == 2:
            sum = hospital_grade_main_call1(grade[index]['grade_url'], grade[index]['grade_name'], locations[location]['location_url'], locations[location]['location_name'], sum)
        else:
            sum = hospital_grade_main_call2(grade[index]['grade_url'], grade[index]['grade_name'], locations[location]['location_url'], locations[location]['location_name'], sum)

    delay = random.uniform(5,7)
    e = time.time()
    print(f"爬取时间为{e - s}s，总共{sum}条数据, 结束时间:{e}")
    print(f"{locations[location]['location_name']}结束, 等待{delay}s开启下一个省份数据的获取")

    time.sleep(delay)  # 延迟 2 秒
    print("-----------------+++++++++++++++++++++++----------------------")





