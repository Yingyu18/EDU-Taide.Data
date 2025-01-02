''''''
# traverse each 題目 
# [ ] 1. 只有第一小題的回答 => 拉掉
# [ ] 2. 只有第二小題的回答 => 使用原題目，排除問題(一)
# [ ] 3. 同時有第一小題和第二小題 整併

import csv
import os
import pandas as pd
import fnmatch  

def extract_sections(text):
    # 初始化結果字典
    sections = {
        "原題目": "",
        "合併題目": "",
        "佳作內容": "",
        "評分評語": ""
    }
    
    # 分割文本為行
    lines = text.split('\n')
    
    current_section = None
    
    for line in lines:
        # 判斷段落開始
        if line.startswith("原題目："):
            current_section = "原題目"
        elif line.startswith("合併題目："):
            current_section = "合併題目"
        elif line.startswith("佳作內容"):
            current_section = "佳作內容"
        elif line.startswith("評分評語：") or line.startswith("評語：") or line.startswith("【評語】") or line.startswith("【評分評語】") :
            current_section = "評分評語"
            
        
        # 如果有當前段落，則添加內容
        if current_section and line:
            # 移除段落標題
            if line.startswith(current_section):
                line = line[len(current_section) + 1:].strip()
            sections[current_section] += line + "\n"
    
    # 清理結果（移除多餘的空白和換行）
    for key in sections:
        sections[key] = sections[key].strip()
    
    return sections

def txt2csv(section, output_path):
    processed_section = {
        key: value.replace('\n', ' ') for key, value in section.items()
    }
    fieldnames = ['原題目', '合併題目', '佳作內容', '評分評語']
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(processed_section)
    print(f"Data has been written to {output_path}")
    

topic_path = "國語文中心/已合併題目"
#（一）
# 問題一
def read_topic():
    for item in os.listdir(topic_path):
        # print(item)
        with open(f"{topic_path}/{item}", "r") as file:
            text = file.read()
            section = extract_sections(text)
            item = item.replace("txt", "csv")
            output_dir = "國語文中心/已合併題目csv"
            os.makedirs(output_dir, exist_ok=True)
            txt2csv(section, f"{output_dir}/{item}")
            # content = section["佳作內容"]
            # if (len(content) > 500 ):
            #     if ( ("（一）" in content or "問題一" in content)):
            #         continue
            #     else: 
            #         print(item)
            # txt2csv 
        continue

def main():
    print(os.getcwd())
    read_topic()
    
if __name__ == "__main__":
    main()
    
    
    # for section, content in text.items():
    #     print(f"\n{section}:")
    #     print(content)
    #     print("-" * 50)