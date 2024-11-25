from docx import Document
import os

def read_docx(file_path):
    # 讀取 docx 檔案內容 
    try:
        doc = Document(file_path)      
        full_text = []
        
        題目=""
        答題=""
        評分=""
        question=True
        response=False
        # 段落
        for para in doc.paragraphs:
            if "題目" in para.text:
                continue
            if "答題" in para.text:
                question=False
                continue
            if "評分" in para.text:
                評分=para.text.strip("評分： ")
                if 評分=="16" or 評分=="17":
                    評分="B+"
                elif 評分=="22" or 評分=="23":
                    評分="A+"
                else:
                    評分="A"
                break
            if question==True:
                題目+=para.text
            else:
                答題+=para.text

            if para.text.strip():  # 排除空白段落
                full_text.append(para.text)
        
        res = { 
            "題目":題目,
            "答題":答題,
            "評分":評分
        }
        print(res)
        return res
        
    except Exception as e:
        print(f"讀取 docx 檔案時發生錯誤: {e}")
        return None