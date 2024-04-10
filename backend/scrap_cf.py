import json
import requests
import os
from config import API_CODEFORCES_PROBLEMSET_LIST

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

else:
    print("Failed to fetch data from the API.")
