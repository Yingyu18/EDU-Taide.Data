import os
'''Description: 整理國師作文的題目'''
file_path = '題目.txt'

with open("國師/題目.txt", "r") as file:
    content = file.read()
    
questions = content.split("****")

# Directory to save the separated files
output_directory = "國師/題目"

# Process each question and save it to a new .txt file
for question in questions:
    # Remove any leading or trailing whitespace
    # question = question.strip()
    
    if question:  # Check if the question is not empty
        # Extract the year from the beginning of the question
        year = question.split("\n", 1)[0].strip()

        # Prepare the filename using the extracted year
        output_file = os.path.join(output_directory, f"{year}.txt")
        
        # Write the question to a new file
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(question[5:])
        
        print(f"Saved question for year {year} to {output_file}")