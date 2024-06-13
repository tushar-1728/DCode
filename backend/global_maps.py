import json


# Codeforces
prob_ratings = list(range(800, 3600, 100))

for prob_rating in prob_ratings:
    map_name = f"mapOfProbRating{prob_rating}"
    globals()[map_name] = {}
    
    with open(f'cf-rating-problems/{prob_rating}.json', 'r') as f:
        problems = json.load(f)

    key = 1
    for problem in problems:
        contestIdFull = str(problem["contestId"]) + problem["index"]
        globals()[map_name][contestIdFull] = key
        key += 1