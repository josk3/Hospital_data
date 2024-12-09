<div align="center">

# 医院数据的获取，数据来源：[丁香园](https://y.dxy.cn/hospital/?)
    
python + BeautifulSoup 实现

<p align="center">
    <img src="https://img.shields.io/badge/Python-3.8+-blue" alt="license">
</p>
</div>  

#### 介绍
获取**丁香园**所有医院具体的数据信息（有：三甲、三乙、三丙、三级、二甲、二乙、二丙、二级、一甲、一乙、一丙、一级、未定级），存储的信息：
<img width="1304" alt="image" src="https://github.com/user-attachments/assets/4c029ccf-6214-4422-9dbd-8c36dafa488c">


#### 特点
1. 使用了 BeautifulSoup 自动。
2. 使用了 time.sleep 的休眠，保证安全，不会出现被封禁的可能。
<img width="319" alt="image" src="https://github.com/user-attachments/assets/3f4d36f1-24e7-4480-a463-7737e92ed5e8">

3. 只要在 main.py 运行，就可以保证全自动进行获取数据。
4. 获取的数据会自动存储在 Excel 表格中，无需手动去添加。
添加到每个地区的文件中：
<img width="752" alt="image" src="https://github.com/user-attachments/assets/7e23f5ae-8e24-47be-a976-dcbc4f751b09">

每个地区文件对应每个等级类型的医院：
<img width="783" alt="image" src="https://github.com/user-attachments/assets/f20c8537-598c-42f3-8b2f-8141e082c9af">

具体的（三甲）：
<img width="1304" alt="image" src="https://github.com/user-attachments/assets/34030fff-2651-4281-b447-ff7450d84313">

#### 代码介绍
1. 所有数据 data 都放在 data.py 文件里。
2. 主函数为 main.py，运行这里的文件就可以全自动爬取。
3. main_all.py 包含主要的执行函数。
