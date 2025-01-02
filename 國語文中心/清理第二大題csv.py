import csv
import os
import pandas as pd

directory = f'國語文中心/第二大題.csv'

# for all column find "亂碼" /xa0 /u3000


for item in os.listdir(directory):
    
    rows_with_xa0 = []  # 用于记录包含 \xa0 的行号
    with open(f"{directory}/{item}", "r") as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames
        rows = list(reader)
        row = rows[0]
        
        
        for column, value in row.items():
            if ' \u3000' in value:
                # row[column] = value.replace('\u3000', ' ')
                rows_with_xa0.append((item))
                #print(f"Column: {column}, Value: {value}")
    
    with open(f"{directory}/{item}", "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()  # 写入表头
        writer.writerows(rows)  # 写入所有行
        
    #     for row_index, row in enumerate(reader, start=1):
    #         for col_index, cell in enumerate(row):
    #             if '\xa0' in cell:
    #                 rows_with_xa0.append((row_index, col_index, cell))

    # 输出结果
    if rows_with_xa0:
        print(f"找到 {len(rows_with_xa0)} 处包含 '\\u3000' 的单元格：")
        for item in rows_with_xa0:
            print(f"{item}\n")
    else:
        print("CSV 文件中未找到 '\\u3000'")