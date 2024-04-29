import json

# Load the categorized_words.json file
with open('categorized_words.json', 'r') as f:
    categorized_words = json.load(f)

# Define a function to filter words by category and save to a new JSON file
def save_category(category):
    category_words = categorized_words.get(category, [])
    with open(f'{category}.json', 'w') as f:
        json.dump(category_words, f, indent=4)

# List of categories to split into separate JSON files
categories = ["love", "mental health", "etc"]  # Add more categories as needed

# Split and save each category into separate JSON files
for category in categories:
    save_category(category)
