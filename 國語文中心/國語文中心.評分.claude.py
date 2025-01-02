import anthropic
from dotenv import load_dotenv
import os, re
import csv

load_dotenv()
api_key = os.getenv("Anthropic_key")

client = anthropic.Anthropic(api_key=api_key)

# Replace placeholders like {{題目}} with real values,
# because the SDK does not support variables.

def rate(題目, 作答):
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        temperature=0,
        system="你現在是一名國文老師，請根據評分原則，為作答文章評分，輸出「整體分數」和「寫作維度」分數。\n \n# 評分標準 - 寫作維度（每個維度0-5分）：  \n - 立意：評估主題或論點是否清晰、深刻。   \n- 結構：檢查文章是否組織有序、結構嚴謹。  \n - 修辭：語言的運用是否恰當、有效。   \n- 敘述：評估故事或論述的發展是否充分、合理。   \n- 啟發：核查文章是否具有啟發性，能否引發讀者思考或情感共鳴。 \n- 整體分數（滿分25分）：   \n- A+（22-25分）：立意精切，結構嚴謹，條理清晰，文辭精練，整體具有啟發性或感動人心的力量。   \n- A（18-21分）：立意深刻，結構合理，敘述有序，文辭得當，具反省或感發效果。   \n- B+（14-17分）：立意適當，結構尚可，表達清楚，文辭順暢，觀點平穩，情感表達穩妥。  \n - B（10-13分）：立意尚可，結構稍具，表述大致合宜，觀點屬習見或情感表達較為平淡。   \n- C+（6-9分）：立意較為平淺，表達有限，文章分段隨意，敘述空泛，文辭平凡，觀點粗糙或情意淡薄。  \n - C（1-5分）：立論單薄或空泛，文章結構混亂，敘述邏輯不清，文辭簡陋，觀點錯誤或缺乏情感。   \n- 0分：空白卷，文不對題，或僅抄錄題幹。 \n- 其他考量：   - 若作文為只有一個段落，最高只能給B+（14-17分）。   - 「*」符號表示錯字。若錯字過多，酌情扣分。   \n- 若題目抄錯或未書寫要求的內容，酌情扣分。\n\n\n# Output Format\n*等級: A+\n寫作維度: 立意: X/5, 結構: X/5, 修辭: X/5, 敘述: X/5, 啟發: X/5\n總分: XX/25\n\n*等級: A\n寫作維度: 立意: X/5, 結構: X/5, 修辭: X/5, 敘述: X/5, 啟發: X/5\n總分: XX/25\n\n\n*等級: B+\n寫作維度: 立意: X/5, 結構: X/5, 修辭: X/5, 敘述: X/5, 啟發: X/5\n總分: XX/25\n\n\n*等級: B\n寫作維度: 立意: X/5, 結構: X/5, 修辭: X/5, 敘述: X/5, 啟發: X/5\n總分: XX/25\n\n\n*等級: C+\n寫作維度: 立意: X/5, 結構: X/5, 修辭: X/5, 敘述: X/5, 啟發: X/5\n總分: XX/25\n\n\n*等級: C\n寫作維度: 立意: X/5, 結構: X/5, 修辭: X/5, 敘述: X/5, 啟發: X/5\n總分: XX/25\n\n# Steps\n1.  對作答進行詳細評估，給出「總分」，以及各維度分數。\n2. 嚴格依照 Output Format 輸出分數。請勿輸出其他內容。\n\n",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"題目：{題目}\n作答：{作答}\n\n\n\n"
                    }
                ]
            }
        ]
    )
    
    resContent = response.content[0].text
    
    print(resContent)
    return resContent 

def read_column(csv_file_path):
    column_values = []

    with open(csv_file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        # 獲取第一個欄位的名稱
        first_column_name = csv_reader.fieldnames[0]
        
        # 讀取第一個欄位的所有值
        for row in csv_reader:
            column_values.append(row[first_column_name])
    
    return column_values

def rate_format(rate_content):
    data = {}
    
    grade = re.search(r'等級:\s*([A-F][+-]?)', rate_content)
    if grade:
        data['等級']=grade.group(1)  
    
    dimensions = re.search(r"立意: (\d+)/5, 結構: (\d+)/5, 修辭: (\d+)/5, 敘述: (\d+)/5, 啟發: (\d+)/5", rate_content)
    if dimensions:
        data['立意'], data['結構'], data['修辭'], data['敘述'], data['啟發'] = dimensions.groups()
    
    total_score = re.search(r"總分: (\d+)/25", rate_content)
    if total_score:
        data['總分'] = total_score.group(1)  
        
    return data 
        
topic_path = "國語文中心/已合併題目csv"
# 將清單匯入 array 
vol_list = read_column("國語文中心/國語文中心.01僅長文.csv")

        
def main():
    for vol in vol_list:
        vol = vol.replace("txt", "csv")
        file_path = f"{topic_path}/{vol}"
        # print(file_path)
        with open(file_path, "r") as file:
            reader = csv.DictReader(file)
            rows = list(reader)  # 將 CSV 的所有行讀取為列表
            # 題目=rows[0]["原題目"]
            # 作答=rows[0]["佳作內容"]
            #print("原題目: \n", 題目)
            #print("佳作內容:\n", 作答)  
            #print("-"*50)     
            # rate_content = rate(題目,作答)     
            # format_content = rate_format(rate_content)  
            # print(format_content)
        # for row in rows:
        #     row['等級']=format_content['等級']
        #     row['總分']=format_content['總分']
        #     row['立意']=format_content['立意']
        #     row['結構']=format_content['結構']
        #     row['修辭']=format_content['修辭']
        #     row['敘述']=format_content['敘述']
        #     row['啟發']=format_content['啟發']
        output_path = f'國語文中心/第二大題.csv'
        os.makedirs(output_path, exist_ok=True)    
        print(f"{output_path}/{vol}")
        with open(f"{output_path}/{vol}", 'w', newline='') as file:
            writer = csv.DictWriter(file,fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
        
    
    # rate_submit()
    
if __name__ == "__main__":
    main()