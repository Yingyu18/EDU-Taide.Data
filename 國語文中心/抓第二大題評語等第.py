import csv
import os
import pandas as pd

directory = f'國語文中心/第二大題.csv'
levels = ["A+","A","B+"]
for item in os.listdir(directory):
    with open(f"{directory}/{item}", "r") as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames
        fieldnames.append('老師給分')
        # reader = csv.DictReader(file)
        rows = list(reader)
        if not rows:
            print(f"文件 {item} 為空或無有效數據，跳過處理。")
            continue
        row = rows[0]
        for level in levels:
            if ( level in row['評分評語']):
                print(f"{item} :")
                print(f"老師給分: {level}")
                row['老師給分']=level
                print(row['老師給分'])
                # print(row['評分評語'])
                # print(f"模型給分：{row['總分']}")
                break
    with open(f"{directory}/{item}", "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()  # 写入表头
        writer.writerows(rows)  # 写入所有行
                