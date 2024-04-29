import json

# Path to your JSON file
file_path = "love.json"

# Open the file and read the first 12 lines
with open(file_path, 'r') as file:
    for i in range(3000):
        line = file.readline().strip()
        if line:
            print(line)

