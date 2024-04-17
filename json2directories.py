import os
import json

def create_folders_from_json(file_path, base_path=""):
    print(f"Reading JSON file from {file_path}")
    # Read the JSON file
    with open(file_path, "r") as file:
        data = json.load(file)

    # Recursive function to create folders
    def create_folders(data, current_path):
        if isinstance(data, dict):
            for key, value in data.items():
                new_path = os.path.join(current_path, key)
                os.makedirs(new_path, exist_ok=True)
                print(f"Created folder: {new_path}")
                create_folders(value, new_path)
        elif isinstance(data, list):
            for idx, item in enumerate(data):
                new_path = os.path.join(current_path, str(idx))
                os.makedirs(new_path, exist_ok=True)
                print(f"Created folder: {new_path}")
                create_folders(item, new_path)

    # Start creating folders
    create_folders(data, base_path)

# Path to the JSON file
file_path = "categorized_words.json"

# Base directory
base_directory = ""  # Empty string for current working directory

# Create folders based on JSON data
create_folders_from_json(file_path, base_directory)