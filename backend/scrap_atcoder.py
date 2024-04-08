import json
import os
import requests
from config import API_ATCODER_PROBLEM_INFO
from config import API_ATCODER_PROBLEM_DIFFICULTY


#Function to make json file of problem-list from api
'''
url = API_ATCODER_PROBLEM_INFO
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    
    # Create the directory if it doesn't exist
    directory = "atcoder-problem-list"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Define the path to the JSON file
    file_path = os.path.join(directory, "problem-list.json")
    
    # Write the JSON data to the file
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)
        
    print(f"JSON data has been saved to '{file_path}' successfully.")
else:
    print("Failed to fetch data from the API.")
'''


url = API_ATCODER_PROBLEM_DIFFICULTY
response = requests.get(url)

difficultyList = {}

# Parse JSON response
if response.status_code == 200:
    data = response.json()

    # Iterate over the problems and group them by difficulty ranges
    for problem_id, problem_info in data.items():
        if "difficulty" in problem_info:
            difficulty = problem_info["difficulty"]
            # Calculate the lower bound of the difficulty range
            lower_bound = (difficulty // 200) * 200
            # Update the difficultyList dictionary
            if lower_bound >= -1400:
                if lower_bound not in difficultyList:
                    difficultyList[lower_bound] = []
                difficultyList[lower_bound].append(problem_id)

    # Create directory if it doesn't exist
    directory = "atcoder-problem-list"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Create files for each difficulty range
    for lower_bound, problems in sorted(difficultyList.items()):
        if lower_bound >= -1400:
            upper_bound = lower_bound + 199
            file_name = f"{lower_bound}.json"
            file_path = os.path.join(directory, file_name)
            with open(file_path, "w") as file:
                json.dump(problems, file, indent=4)
            print(f"Created file {file_path} for problems in range {lower_bound} to {upper_bound}")

else:
    print("Failed to fetch data from the API.")
