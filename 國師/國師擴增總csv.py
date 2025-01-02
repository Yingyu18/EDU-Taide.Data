import csv
import re
import os

# f"國師/答題/資料擴增/csv/{dep}/{卷號}/{卷號}-{等第}.csv" 

all_rows = []
all_fieldnames = None

output_file = "國師/答題/資料擴增/總表.csv"
directory = "國師/答題/資料擴增/csv"


fieldnames=[]
for dep in os.listdir(directory):
    if '.DS_Store' not in dep:
        dep_dir = f"{directory}/{dep}"
        for vol in os.listdir(dep_dir):
            if '.DS_Store' not in vol:
                vol_dir = f"{dep_dir}/{vol}"
                for item in os.listdir(vol_dir):
                    print(item)
                    with open(f"{vol_dir}/{item}", "r") as file:
                        reader = csv.DictReader(file)
                        # fieldnames = reader.fieldnames
                        rows = list(reader) 
                            
                        # 若 fieldnames 未初始化
                        if all_fieldnames is None:
                            all_fieldnames = ["vol_num", "level"] + reader.fieldnames
                        # elif all_fieldnames != reader.fieldnames:
                        #     print(f"警告：文件 {item} 的 fields 其他文件不一致，跳過此文件。")
                        #     continue
                        
                        last_dash_index = item.rfind('-')
                        if last_dash_index != -1:
                            vol_num = item[:last_dash_index]  # 提取卷號
                            level = item[last_dash_index + 1:]  # 提取等第
                            level = level[:-4]
                            print(f"卷號: {vol_num}, 等第: {level}")

                        for row in rows:
                            row["vol_num"] = vol_num
                            row["level"]=level
                        # 将当前文件的所有行加入总行列表
                        all_rows.extend(rows)
                        

### 寫進大的總表                 
# with open(f"", "w", encoding="utf-8", newline="") as file:
#     writer = csv.DictWriter(file, fieldnames=fieldnames)
#     writer.writeheader()  # 写入表头
#     writer.writerows(rows)  # 写入所有行
    
if all_fieldnames and all_rows:
    with open(output_file, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=all_fieldnames)
        writer.writeheader()  # 写入表头
        writer.writerows(all_rows)  # 写入所有行
    print(f"所有文件已成功合併為： {output_file}")
