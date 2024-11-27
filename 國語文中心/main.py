''''''
# traverse each 題目 
# [ ] 1. 第一小題的回答 => 拉掉
# [ ] 2. 第二小題的回答 => 使用原題目，排除問題(一)
# [ ] 3. 同時有第一小題和第二小題 整併


import os
import pandas as pd
import fnmatch  

topic_path = "國語文中心/已合併題目"

def read_topic():
    for item in os.listdir(topic_path):
        print(item)
        with open(f"{topic_path}/{item}", "r") as file:
            article = file.read()
            # print(article)
        continue

def main():
    read_topic()
    
if __name__ == "__main__":
    main()
