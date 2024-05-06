import json
import requests
import os
from config import API_CODEFORCES_PROBLEMSET_LIST

# Function to keep only the first 100 objects in a JSON file
def keep_first_100_objects(file_path):
    with open(file_path, "r+") as json_file:
        data = json.load(json_file)
        data["problems"] = data["problems"][:100]
        # Set file pointer to the beginning of the file
        json_file.seek(0)
        # Write the modified JSON data back to the file
        json.dump(data, json_file, indent=4)
        # Truncate the file to remove any remaining content
        json_file.truncate()

url = API_CODEFORCES_PROBLEMSET_LIST
response = requests.get(url)

# Parse JSON response
data = response.json()

# Check if API response is successful
if data.get("status") == "OK":
    problems = data["result"]["problems"]

    # Iterate through each problem
    for problem in problems:
        if "rating" in problem:
            rating = problem["rating"]
            # Ensure rating falls within the specified range
            if 800 <= rating <= 3500:
                # Create directory if it doesn't exist
                directory = os.path.join("cf-rating-problems")
                if not os.path.exists(directory):
                    os.makedirs(directory)
                
                # Write problem details to JSON file
                file_path = os.path.join(directory, f"{rating}.json")
                with open(file_path, "a") as json_file:
                    json.dump(problem, json_file, indent=4)
                    json_file.write("\n")

                # print(f"Problem with rating {rating} saved to {file_path}")

    directory = os.path.join("cf-rating-problems")
    # Iterate through each JSON file in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            file_path = os.path.join(directory, filename)
            # Keep only the first 100 objects in the JSON file
            keep_first_100_objects(file_path)

else:
    print("Failed to fetch data from the API.")
