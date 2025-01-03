# -*- coding: utf-8 -*-
import os
from anthropic import Anthropic 
from dotenv import load_dotenv
import csv
import logging

# 設定 log 寫入檔案
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='國師擴增.log',  # 指定 log 檔案名稱
    filemode='a'         # 使用 'w' 覆寫舊的 log，或 'a' 追加到現有檔案
)

# 加載 .env 文件中的變數
load_dotenv()

# 使用環境變數
api_key = os.getenv("Anthropic_key")


def process_augmentation(id, file_path):
    try:
        client = Anthropic(api_key=api_key)
        # Replace placeholders like {{題目}} with real values,
        # because the SDK does not support variables.
        
        vol = id[0:4]
        dep = id[5:10]
        
        # print(vol, dep)   
        with open(f"{file_path}", 'r', encoding='utf-8') as f:
            # 寫入基本資訊
            答題 = f.read()
        logging.info(答題)
        # print(答題)
        
        file_path = f'國師/題目/{vol}.txt'   
        with open(file_path, 'r', encoding='utf-8') as f:
            # 寫入基本資訊
            題目 = f.read()      
        logging.info(題目)    
        # print(題目)

    
        # levels = ["A+","A","B+", "B", "C+", "C"]
        # levels = ["A+","C"]
        # levels = ["C+"]
        # levels = ["A"]
        # levels = ["A+"]
        levels = ["C"]
        
        for level in levels:
            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1000,
                temperature=0,
                system=f"你現在是一位文字工作者，任務是要改寫文章。請依據給定的評分標準和答題，調整答題文章在評分原則中五個向度的水準，將原本級的文章改寫為{level}等級的文章。輸出改寫文章，並為改寫文章輸出「整體分數」和「寫作維度」分數。請勿輸出其他內容。\n\n# 評分標準\n\n- 寫作維度（每個維度0-5分）：\n  - 立意：評估主題或論點是否清晰、深刻。\n  - 結構：檢查文章是否組織有序、結構嚴謹。\n  - 修辭：語言的運用是否恰當、有效。\n  - 敘述：評估故事或論述的發展是否充分、合理。\n  - 啟發：核查文章是否具有啟發性，能否引發讀者思考或情感共鳴。\n\n- 整體分數（滿分25分）：\n  - A+（22-25分）：立意精切，結構嚴謹，條理清晰，文辭精練，整體具有啟發性或感動人心的力量。\n  - A（18-21分）：立意深刻，結構合理，敘述有序，文辭得當，具反省或感發效果。\n  - B+（14-17分）：立意適當，結構尚可，表達清楚，文辭順暢，觀點平穩，情感表達穩妥。\n  - B（10-13分）：立意尚可，結構稍具，表述大致合宜，觀點屬習見或情感表達較為平淡。\n  - C+（6-9分）：立意較為平淺，表達有限，文章分段隨意，敘述空泛，文辭平凡，觀點粗糙或情意淡薄。\n  - C（1-5分）：立論單薄或空泛，文章結構混亂，敘述邏輯不清，文辭簡陋，觀點錯誤或缺乏情感。\n  - 0分：空白卷，文不對題，或僅抄錄題幹。\n\n- 其他考量：\n  - 若作文為只有一個段落，最高只能給B+（14-17分）。\n  - 「*」符號表示錯字。若錯字過多，酌情扣分。\n  - 若未書寫要求的內容，酌情扣分。\n\n# Output Format\n寫作維度: 立意: X/5, 結構: X/5, 修辭: X/5, 敘述: X/5, 啟發: X/5\n總分: XX/25\n\n# Steps\n1. 根據上述每個「寫作維度」對答題作文不同維度進行等級調整，改寫為另一篇文章。\n2. 對改寫文章進行詳細評估，給出「整體分數」，以及各維度分數。\n3. 嚴格依照 Output Format 輸出分數。請勿輸出其他內容。",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            # {
                            #     "type": "text",
                            #     "text": "<examples>\n<example>\n<答題>\n在網路迅速發展的時代，人類的記憶力到底是會衰退，還是隨著科技愈發博學多聞？我想這必須考慮到：是「人使用網路」抑或是「人依賴網路」？一旦網路消失了，人們會再創顛峰，又或是自甘墮落？\n\n我對網路的發展是抱持著正向的想法的，也許有人認為這不利於認知學習，但對於一個極需在其專業領域上發揮創造力的人而言，若是自小被教育了許多過去人認為是對的「知識」，那他要如何跳脫框架思考？正因為「網路」的言論充滿了不確定性，才促使一個人產生懷疑而充滿好奇，進而做更深入的研究。正因為懷疑，哥白尼才提出日心說，才顛覆了千年來人們的信念。\n\n對一個科學家或是發明家來說，毋須記憶大量知識才更能顛覆固有思考，進而專精在自己所學，並且在使用網路時記憶下對研究有助的學說，也許哪一天也能再創科學界的顛峰！這樣的思維模式使得人們能夠從現有的資訊中抽取關鍵，並且將其與自己的知識相結合，從而形成更具創意的觀點和解決方案。以此而言，網路不僅是知識的載體，更是創新思維的重要工具。\n\n然而，若完全依賴網路，則可能導致思考的淺薄和記憶的衰退。對於學習而言，記憶的過程仍是關鍵的一環。人類的記憶力在某種程度上與對知識的理解和應用能力息息相關，因此若能在網路的輔助下，兼顧自主學習和知識的儲存，或許能讓我們在科技發展的浪潮中更加茁壯。\n\n此外，網路的發展也要求教育者重新思考教學的方式。傳統的知識傳授模式應該轉變為培養學生的批判性思維和解決問題的能力。鼓勵學生在探索網路資訊的同時，發展出獨立思考的能力，這樣才能在未來的社會中適應不斷變化的環境。\n\n總結來說，網路的發展無疑改變了我們獲取和處理資訊的方式，關鍵在於如何使用這一工具。透過合理的方式運用網路，將有助於提升人類的創造力與學習能力；反之，過度依賴則可能使我們逐漸失去思考的能力。因此，在面對科技進步的同時，我們更應該思考如何平衡網路使用與自主學習的關係，才能讓記憶力與思考力持續增長。\n\n</答題>\n<題目>\n自從有了電腦、智慧型手機及網路搜尋引擎之後，資訊科技的發展改變了人類大腦處理資訊的方式。我們可能儲存了大量的資訊，卻來不及閱讀，也不再費力記憶周遭事物和相關知識，因為只要輕鬆點一下滑鼠、滑一下手機，資訊就傳到我們面前。\n二十一世紀資訊量以驚人的速度暴增，有人認為網路資訊易於取得，會使記憶力與思考力衰退，不利於認知學習；也有人視網際網路為人類的外接大腦記憶體，意味著我們無須記憶大量知識，而可以專注在更重要、更有創造力的事物上。對於以上兩種不同的觀點，請提出你個人的看法。文長限700字內。\n\n</題目>\n<原等級>\nA\n</原等級>\n<改寫等級>\nC\n</改寫等級>\n<ideal_output>\n現在的人都在用網路，每天都在滑手機，很少人會想要去記東西。我覺得這樣不太好，因為人應該要多動腦想事情，不能都靠網路。\n網路雖然可以讓我們找到很多資料，但是我覺得還是要自己記東西比較好。像我以前都很認真讀書，自己記筆記，成績就很好。現在的同學都只會用手機，什麼都不記，上課也不認真聽，都在玩手機，這樣很浪費時間。\n網路也不是說有多好，因為網路上有很多錯誤的資料。而且網路會讓人變笨，因為大家都不想要思考，看到什麼都直接相信。我認為人還是要自己動腦想，不能完全靠網路。\n很多人說網路很好用，可以讓我們不用記那麼多東西。但是我覺得這樣不行，因為如果都沒有記憶，人的大腦就會變成空的，什麼都不會。而且網路有時候會壞掉，如果那時候找不到資料怎麼辦？\n所以我希望大家可以少用一點網路，多用腦袋想事情。網路應該只是一個輔助工具，不能變成我們的大腦。我們要記住，人比網路還要厲害！\n\n</ideal_output>\n</example>\n</examples>\n\n"
                            # },
                            {
                               "type": "text",
                                "text": "<examples>\n<example>\n<題目>\n二十一世紀資訊量以驚人的速度暴增，有人認為網路資訊易於取得，會使記憶力與思考力衰退，不利於認知學習；也有人視網際網路為人類的外接大腦記憶體，意味著我們毋須記憶大量知識，可以專注在更重要、更有創造力的事物上。對於以上兩種不同的觀點，你的看法為何？請以「網海浮沉之我思」為題，結合自己的相關經驗，探討創造力與思考力之間的關係。\n文長至少600字。\n</題目>\n<答題>\n        網海浮沉之我思\n    在網路如此發達的世代，獲得資訊簡直易如反掌，能在短時間內接收大量的資訊，甚至利用更專業的應用程式整理或分類所得知的知識，網路的便捷提升人們的效率。\n    身為學生的我除了做好學習的本份*，更重要的是多元的學習，而網路便成為我最方便的工具，當面對一篇英語文章內容有許多陌生的字詞時，我便可以利用網路快速查找其字義，甚至可以利用某些軟體統整自己不熟悉的單字。這樣既節省以往查字典的時間，也很大的提升讀書的效率，也可利用多出來的時間去查找該科的相關資訊，為自己補充更多所感興趣的知識。\n    雖然網路如此便利，我們可快速獲取大量資訊，可網路上的資訊有真有假，若是一昧的複製、貼上，毫無自己的判斷，甚至對於所得知的資訊未經自己的思考，未有自己的看法，那又如何稱作學習呢？學習應是在接收新的知識後，經過自己的思考，判斷哪些資訊是需要的，並且將資訊利用自己能夠理解的方式加以統整歸納，將那些知識變成自己的，否則無論網路有多麼便利，未有自己的認知，那也是浪費了如此方便的工具，使它失去其存在的意義。\n    在如今的網路時代，也許很多人都使用過網路，可不僅如此，我們更應該善用網路。網路只是個工具，更重要的是我們如何利用它，提升自己，並且不過度依賴。在使用網路時，應有自己的思考，讓它成為真正有幫助的輔助工具。\n</答題>\n<改寫等級>\nA\n</改寫等級>\n<ideal_output>\n網海浮沉之我思\n\n在這個數位洪流席捲的二十一世紀，資訊的獲取已變得前所未有的便利。每當我們徜徉在浩瀚的網海中，總不禁思索：這樣的便利究竟是增進還是消弭了我們的認知能力？這個問題值得我們深入探討。\n\n就個人經驗而言，網路確實大幅改變了我的學習模式。當我在研讀英文文獻時，不再需要在厚重的字典中翻找，取而代之的是快速精準的線上查詢；面對艱深的學術概念，各種線上教學資源也為我打開了新的認知之窗。這些便利確實為學習帶來了前所未有的效率，讓我們能夠將更多心力投注在知識的深化與創新運用上。\n\n然而，這把雙刃劍也帶來了潛在的危機。在資訊唾手可得的同時，我觀察到許多人逐漸養成了「快速瀏覽，淺層理解」的習慣。這種現象就像是在知識的海洋中浮游，卻始終無法深潛至知識的核心。更令人憂心的是，網路資訊良莠不齊，若缺乏批判思考能力，極易陷入以訛傳訛的迷思中。\n\n因此，我認為重點不在於是否使用網路，而在於如何善用它。網路應該被視為強化思考的工具，而非替代思考的捷徑。當我們在網路上搜尋資訊時，更應該培養「深度學習」的習慣：先確認資訊的可靠性，再透過分析、整合與反思，將外在知識內化為自己的認知體系。\n\n創造力與思考力的關係，恰如種子與土壤。網路提供了豐富的養分，但若要讓創意之花綻放，仍需要透過深度思考這片沃土來培育。我們應該善用網路擴展視野，但同時保持獨立思考的能力，讓資訊科技真正成為知識創新的助力，而非阻力。\n\n在這個資訊爆炸的時代，與其被動地被資訊淹沒，不如主動地駕馭資訊之舟。唯有在汪洋般的網海中保持清醒的思考，才能真正駛向知識的彼岸，創造出屬於自己的航道。\n\n寫作維度: 立意: 5/5, 結構: 4/5, 修辭: 4/5, 敘述: 4/5, 啟發: 4/5\n總分: 21/25\n</ideal_output>\n</example>\n</examples>\n\n"
                            },
                            {
                                "type": "text",
                                "text": f" 題目：{題目}\n\n\n\n 答題：{答題}\n\n請將此篇文章改寫為{level}級文章，輸出文章並從五個寫作維度替此篇 {level} 級文章評分。"
                            }
                        ]
                    }
                ]
            )
            
            resContent = response.content[0].text
            print(resContent)
            create_augmentation_file(id, level, resContent)
            
            new_row = {"檔案名稱": id, "等級": level}
            with open('國師/答題/已擴增作答.csv', mode="a", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=["檔案名稱", "等級"])
                writer.writerow(new_row)
                print(f"Added: {new_row} to 已擴增作答.csv")
        
    except Exception as e:
        print(f"處理內容時發生錯誤: {e}")    
        logging.error(e)    
        
def create_augmentation_file(id, level, content):
        vol = id[0:4]
        dep = id[5:10]
        # # 建立檔案名稱
        file_name = f"{id}-{level}.txt"
        output_dir = f"國師/答題/資料擴增/{dep}/{id}"
        os.makedirs(output_dir, exist_ok=True)
        
        # # 完整檔案路徑
        file_path = os.path.join(output_dir, file_name)     
        
        # 將結果寫入檔案
        with open(file_path, 'w', encoding='utf-8') as f:
            # 寫入基本資訊
            f.write(content)
        
        print(f"已儲存結果至：{file_path}")   
        logging.info(f"已儲存結果至：{file_path}")
        
           
def process_multiple_files():
    dep_list=[]
    with open('國師/答題/資料擴增/dep_C.csv', mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        
        # 取得標題行
        header = next(reader)
        target_index = header.index("dep")  # 找到目標欄位的索引
        # 提取目標欄位的資料
        for row in reader:
            dep_list.append(row[target_index])  # 讀取特定欄位值
            
    directory = f"國師/答題"
    count = 0
    for dep in dep_list:
        if dep == ".DS_Store" or dep == '已擴增作答.csv':
            continue
        dep = os.path.join(directory, dep)
        for folder in os.listdir(dep):
            folder = os.path.join(dep, folder)
            for root, dirs, files in os.walk(folder):
                for file in files:
                    count+=1
                    file_path = os.path.join(root, file)
                    # if file == "1071-01-02-113407026.txt":
                    process_augmentation(file.strip(".txt"), file_path)
                
                
    print(count)
    # with open('國師/答題/資料擴增/dep_list.csv', mode='w', newline='', encoding='utf-8') as file:
    #     writer = csv.writer(file)
        
    #     # 寫入標題行（可選）
    #     writer.writerow(["Column1"])
        
    #     # 寫入資料，每個值一行
    #     for value in dep_list:
    #         writer.writerow([value])  # 單一欄位
    
def main():
    # 首先安裝必要套件
    # pip install python-docx anthropic
    process_multiple_files()
    
if __name__ == "__main__":
    main()
