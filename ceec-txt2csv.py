import csv, re, os

# Define a function to extract fields from the text
def parse_txt_file(filename):
    data = {}
    '''Combine 題目'''
    year = ""
    # Regular expression pattern to capture the year
    pattern = r"ceec-(\d+)-\d+-[A-Z]+\+?\.txt"  

    # Extract the year using re.search
    match = re.search(pattern, filename)
    if match:
        year = match.group(1)
        print(f"Extracted year: {year}")
    else:
        print("Year not found in the string.")    
        
    with open(f"file/題目/{year}.txt", 'r', encoding='utf-8') as file:    
        data["題目"] = file.read()
        
    '''Read .txt file'''
    with open(filename, 'r', encoding='utf-8') as file:    
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
    nos = ["1", "2", "3", "4", "5"]
    years = ["113","112", "111", "108", "109", "110", "107"]
    # nos = ["6"]
    
    for year in years:
        for no in nos:
            # file_path = f"./file/{year}/ceec-{year}-{no}.docx"
            directory = f"./file/{year}/ceec-{year}-{no}"
            if os.path.exists(directory):
                for root, dirs, files in os.walk(directory):
                    count = 0
                    for file in files:
                            if file.endswith('.txt'):
                                count+=1
                                #print(file)
                                file_path = os.path.join(root, file)
                                # if file == "ceec-112-5-A+.txt":
                                content = parse_txt_file(file_path)
                                file = file.replace("txt", "csv")
                                directory_path = f"file/ceec-csv/{year}/ceec-{year}-{no}"
                                os.makedirs(directory_path, exist_ok=True)
                                write_to_csv(content, f"{directory_path}/{file}")
                    # print(directory, count)

if __name__ == "__main__":
    main()
