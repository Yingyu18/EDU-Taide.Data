'''學測98-106年度'''
'''多個佳作csv 整併為單一 csv'''
# TODO: 未來將擴增作文合併為單一 csv時，要注意不混淆原卷和擴增作文 

import csv
import os

# f"國師/答題/資料擴增/csv/{dep}/{卷號}/{卷號}-{等第}.csv" 

all_rows = []
all_fieldnames = None

output_file = "學測98-106/csv/佳作總表.csv"
directory = "學測98-106/csv"



def main():
    global all_fieldnames
    fieldnames=[]
    for year in os.listdir(directory):
        if '.DS_Store' in year:
            continue
        year_dir = f"{directory}/{year}"
        for vol in os.listdir(year_dir): 
            if '.DS_Store' in vol:
                continue
            vol_dir = f"{year_dir}/{vol}"
            for item in os.listdir(vol_dir):
                print(item)
                with open(f"{vol_dir}/{item}", "r") as file:
                    reader = csv.DictReader(file)
                    # fieldnames = reader.fieldnames
                    rows = list(reader) 
                        
                    # 若 fieldnames 未初始化
                    if all_fieldnames is None:
                        all_fieldnames = ["vol_num"] + reader.fieldnames
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
                        #row["level"]=level
                        
                    # 将当前文件的所有行加入总行列表
                    all_rows.extend(rows)
                    
    if all_fieldnames and all_rows:
        with open(output_file, "w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=all_fieldnames)
            writer.writeheader()  # 写入表头
            writer.writerows(all_rows)  # 写入所有行
        print(f"所有文件已成功合併為： {output_file}")




if __name__ == "__main__":
    main()