import csv, re, os

# Define a function to extract fields from the text
def parse_txt_file(filename, file_path):
    data = {}
    '''Combine 題目'''
    parts = filename.split('-')

    # 解析各欄位
    year = parts[0]       # 題目年份
    dep = f"{parts[1]}-{parts[2]}" # 系所
    number = parts[3]     # 編號

        
    with open(f"國師/題目/{year}.txt", 'r', encoding='utf-8') as file:    
        data["題目"] = file.read()
        
    '''Read .txt file'''
    with open(file_path, 'r', encoding='utf-8') as file:    
        lines = file.readlines()
        
        # Combine lines to capture the content of the answer and fields more accurately
        content = "".join(lines)
        
        # Extract scores from the structured lines
        dimensions = re.search(r"立意: (\d+)/5, 結構: (\d+)/5, 修辭: (\d+)/5, 敘述: (\d+)/5, 啟發: (\d+)/5", content)
        if dimensions:
            data['立意'], data['結構'], data['修辭'], data['敘述'], data['啟發'] = dimensions.groups()
        
        total_score = re.search(r"總分: (\d+)/25", content)
        
        if total_score:
            data['總分'] = total_score.group(1)
            
        # Extract fields using regular expressions
        first_line = content.split('\n')[0]  # Assumes the first line is the question
        if "寫作維度" not in first_line:
            data['作答'] = "\n".join(lines[0:-2]).strip()  # Assumes answer ends before "寫作維度:"
        else:
            data['作答'] = "\n".join(lines[2:]).strip()
    
    return data

# Convert parsed data to CSV
def write_to_csv(parsed_data, output_csv):
    fieldnames = ['題目', '作答', '立意', '結構', '修辭', '敘述', '啟發', '總分']
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(parsed_data)
    print(f"Data has been written to {output_csv}")

def main():
    
    field_names = [str(i) for i in range(1, 26)]

    # 創建一個空表格（模擬為多行資料的列表，每行是字典）
    table = []

    # 新增一列資料
    row = {field: 0 for field in field_names}  # 使用 None 作為初始值
    table.append(row)
    table = table[0]
    print(table)
    
    directory = "國師/答題/資料擴增"
    file_name = "已生成A檔案.csv"
    deps = []
    with open(f'國師/答題/資料擴增/{file_name}', mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        
        # 取得標題行
        header = next(reader)
        target_index = header.index("dep")  
        # 提取目標欄位的資料
        for row in reader:
            deps.append(row[target_index])  # 讀取特定欄位值
                
    for dep in deps:
        #print(dep)
        dep_path = f"{directory}/{dep}"
        if os.path.exists(dep_path):
            for root, dirs, files in os.walk(dep_path):
                count = 0
                for dir in dirs:
                    # print(dir)
                    dir_path = f"{dep_path}/{dir}"
                    #print(dir_path)
                    for root, dirs, files in os.walk(dir_path):
                        for file in files:
                            # if file.endswith('.txt'):
                            file_path = os.path.join(root, file)
                            #print(file_path)
                            # if file == "ceec-112-5-A+.txt":
                            content = parse_txt_file(file, file_path)
                            
                            if content.get('總分'):
                                print(content['總分'])
                                table[content['總分']]+=1
                            file_name = file.replace("txt", "csv")
                            output_path = f"{directory}/csv/{dep}/{dir}"
                            os.makedirs(output_path, exist_ok=True)
                            #print(output_path)
                            #write_to_csv(content, f"{output_path}/{file_name}")
                    # print(directory, count)
    print(table)



if __name__ == "__main__":
    main()
