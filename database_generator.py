from openai import OpenAI
import os
from collections import defaultdict
import json

# Create OpenAI instance
client = OpenAI(api_key="sk-proj-DUB4qdxFJl4JCJCBepndT3BlbkFJsaqdzEoCHwNMJlXfVMLq")

# Define the llm_call function
def llm_call(system_content, user_content):
    completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": system_content},
        {"role": "user", "content": user_content}
      ]
    )

    return completion.choices[0].message.content

# Function to categorize words
def categorize_words(words):
    print("Categorizing words:", words)
    categorized_words = defaultdict(lambda: defaultdict(list))

    # Construct the system content
    system_content = "You take in affirmations and categorize their words into JSON-like structure. Each affirmation is broken down into affirmunits, which are meaningful phrases capturing specific aspects of the overall message, excluding common grammatical parts like prepositions and conjunctions. You are not allowed to be vague or general, and each grammarrole-subject-affirmunit link should be highly specific to the pt that there sould only be about 20 affirmunits per each grammar-subject link if that makes sense.Here are examples of affirmunits within affirmations:\n" \
                 "1. Affirmation: \"I am worthy of love and respect.\"\n" \
                 "   - Affirmunits:\n" \
                 "     - \"I am worthy\"\n" \
                 "     - \"love and respect\"\n" \
                 "2. Affirmation: \"I embrace my uniqueness and celebrate who I am.\"\n" \
                 "   - Affirmunits:\n" \
                 "     - \"I embrace my uniqueness\"\n" \
                 "     - \"celebrate who I am\"\n" \
                 "3. Affirmation: \"I attract positive energy and abundance into my life.\"\n" \
                 "   - Affirmunits:\n" \
                 "     - \"I attract positive energy\"\n" \
                 "     - \"abundance into my life\"\n" \
                 "4. Affirmation: \"I am confident and capable of achieving my goals.\"\n" \
                 "   - Affirmunits:\n" \
                 "     - \"I am confident\"\n" \
                 "     - \"capable of achieving my goals\"\n" \
                 "5. Affirmation: \"I am grateful for all the blessings in my life.\"\n" \
                 "   - Affirmunits:\n" \
                 "     - \"I am grateful\"\n" \
                 "     - \"all the blessings in my life\"\n" \
                 "Categorize the affirmunits according to their meaning and context, and structure the output in a JSON-like format.\n" \
                 "{\n" \
                 "    \"Noun\": {\n" \
                 "        \"romantic\": [\n" \
                 "            \"safe, enjoyable sex\",\n" \
                 "            \"attractive trans girls\",\n" \
                 "            \"positive energy\"\n" \
                 "        ],\n" \
                 "        \"selfesteem\": [\n" \
                 "            \"person of value\"\n" \
                 "        ],\n" \
                 "        \"spiritual\": [\n" \
                 "            \"worthy of love\"\n" \
                 "        ]\n" \
                 "    },\n" \
                 "    \"Adjective\": {\n" \
                 "        \"selfesteem\": [\n" \
                 "            \"worthy of attention\",\n" \
                 "            \"unique\"\n" \
                 "        ]\n" \
                 "    },\n" \
                 "    \"Verb\": {\n" \
                 "        \"social\": [\n" \
                 "            \"genuinely like me\",\n" \
                 "            \"attract\"\n" \
                 "        ]\n" \
                 "    }\n" \
                 "}"

    # Instruct AI to categorize words
    json_string = llm_call(system_content, " ".join(words))

    # Parse JSON-like string output
    try:
        categorized_data = json.loads(json_string)
    except json.JSONDecodeError as e:
        print("Error parsing JSON:", e)
        return {}

    # Convert the data to the desired format
    for category, words_dict in categorized_data.items():
        for word, tags in words_dict.items():
            for tag in tags:
                categorized_words[tag][category].append(word)

    return categorized_words

# Function to process affirmations in text files
def process_text_file(file_path):
    print("Processing file:", file_path)
    with open(file_path, 'r') as file:
        text = file.read()
        words = [word.strip() for word in text.split(',')]
        return categorize_words(words)

# Function to process affirmations in all text files in subdirectories
def process_all_files_in_subdirectories(root_dir):
    print("Processing all files in subdirectories of:", root_dir)
    affirmations_data = defaultdict(lambda: defaultdict(list))

    # Iterate over subdirectories
    for subdir, dirs, files in os.walk(root_dir):
        # Iterate over files in each subdirectory
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(subdir, file)
                category = os.path.basename(subdir)
                affirmations_data[category].update(process_text_file(file_path))

    return affirmations_data

# Main function
def main():
    # Get current working directory
    cwd = os.getcwd()
    print("Current working directory:", cwd)

    # Process all text files in subdirectories
    affirmations_data = process_all_files_in_subdirectories(cwd)
    print("Categorized words:", affirmations_data)

    # Output categorized affirmations as JSON
    with open('categorized_words.json', 'w') as json_file:
        json.dump(affirmations_data, json_file, indent=4)

    print("Categorized words saved to categorized_words.json")

if __name__ == "__main__":
    main()