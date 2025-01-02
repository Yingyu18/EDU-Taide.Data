''' 
Description: Save each article as txt file and named with 卷號 amd 文章流水號

next step: combine the statements and the articles respectively as the input to Claude to generate
different levels articles  
'''
# Task 1: Write up [題目.txt]
# Task 2: identify states by 「評分表-總表」  流水號->卷號  
# Task 3: identify article from [打字區] using 卷號

'''from 評分表總表'''
import os
import pandas as pd
import fnmatch  



def search_in_folders(directory):
    for item in os.listdir(directory):
        path = os.path.join(directory, item)
        prefix = school
        if os.path.isdir(path) and fnmatch.fnmatch(item, prefix + "*"):
            #print(f"Entering folder: {path}")
            prefix = dep
            directory = path
            for item in os.listdir(directory):
                path = os.path.join(directory, item)
                if os.path.isdir(path) and fnmatch.fnmatch(item, prefix + "*"):
                    print('search folder: ', path)
                    search_file(path)
                
            

def search_file(directory):            
    for item in os.listdir(directory):
        if item == f"{article_id}.txt":
            article = ""
            try: 
                '''read the article'''
                path = os.path.join(directory, item)
                print(path)
                with open(path, "r") as file:
                    # print(path)
                    article = file.read()
            except Exception as e:
                print(f"讀取檔案遇到問題： {e}")   
                
            # print(article)
            ''' use 題目ID as the file name '''
            output_file = f"國師/答題/{school}-{dep}/{vol}-{article_id}/{vol}-{article_id}.txt"
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            try:
                with open(output_file, "w", encoding="utf-8") as file:
                    file.write(article)
            except UnicodeDecodeError:
                print(f"Error reading {file_path}: Unable to decode in UTF-8. Skipping this file.")
 
'''讀取評分表'''
# .xlsx 檔名 = 拿到 0x0x 作為打字區追蹤  
# 卷號 作為 題目.txt 追蹤

#directory = "國師/評分表"
directory = "國師/評分表20241205"
print(os.getcwd())

count=0 
# Traverse all .xlsx files in the directory
for root, dirs, files in os.walk(directory):
    for file in files:
        #if count == 0:
        print(file)
        if file.endswith('.xlsx'):
            file_path = os.path.join(root, file)
            
            # Load the Excel file
            excel_file = pd.ExcelFile(file_path)
            sheet_name = excel_file.sheet_names[0]
            df = pd.read_excel(file_path, sheet_name=sheet_name)
    
            school = file[0:2]
            dep = file[2:4]
            
            '''iterate each volume and combine 題目, article'''
            for index, row in df.iterrows():
                count+=1
                vol = row['卷號']
                article_id  = row['流水號']

                '''Access article by school and dep and 流水號'''
                prefix = school                   
                # search_in_folders("國師/打字區")
                
print(count)






