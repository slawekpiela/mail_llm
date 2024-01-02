def add_newlines_to_keywords(file_path, keywords):
    # Read the content of the file
    with open(file_path, 'r') as file:
        content = file.read()

    # Replace each keyword with keyword + newline
    for keyword in keywords:
        content = content.replace(keyword, keyword + '\n')

    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.write(content)

# Usage
file_path = 'your_file.txt' # Replace with your file path
keywords = ['question', 'answer', 'section']
add_newlines_to_keywords(file_path, keywords)
