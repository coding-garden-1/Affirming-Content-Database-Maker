import json

# Path to your JSON file
file_path = "your_file.json"

# Open the file and read the first 12 lines
with open(file_path, 'r') as file:
    for i in range(12):
        line = file.readline().strip()
        if line:
            print(line)

