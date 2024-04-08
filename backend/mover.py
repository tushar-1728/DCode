import os
import json

# Function to read JSON file
def read_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Function to write JSON file
def write_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# Read problem list
problem_list = read_json('atcoder-problem-list/problem-list.json')

'''
# Delete existing rating JSON files
for rating in range(-1400, 4201, 200):
    rating_file_path = f'atcoder-rating/{rating}.json'
    if os.path.exists(rating_file_path):
        os.remove(rating_file_path)
'''
'''
# Iterate over rating JSON files
for rating in range(-1400, 4201, 200):
    rating_file_path = f'atcoder-rating-problems/{rating}.json'
    rating_data = read_json(rating_file_path)

    # Filter out problems with matching IDs
    matched_problems = []
    for problem_id in rating_data:
        for problem in problem_list:
            if problem_id == problem['id'] and not problem['name'].startswith('\\'):
                matched_problems.append({
                    'id': problem['id'],
                    'contest_id': problem['contest_id'],
                    'name': problem['name']
                })
                break

    # Write matched problems to new JSON file
    output_folder = 'atcoder-rating'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    output_file_path = f'{output_folder}/{rating}.json'
    write_json(output_file_path, matched_problems)
'''