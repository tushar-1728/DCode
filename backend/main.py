from flask import Flask, request, redirect, render_template, render_template_string, jsonify
from flask.helpers import url_for
from config import API_CODEFORCES_USER_INFO, API_CODEFORCES_USER_PROBLEM_STATUS, API_ATCODER_USER_CONTEST_INFO, API_CODEFORCES_USER_CONTEST_INFO, API_ATCODER_USER_PROBLEM_STATUS
from dotenv import load_dotenv
from collections import Counter

import os, time
import json, requests
import global_maps


# Load environment variables from .env file
load_dotenv()

app = Flask("DCODE")
app.secret_key = os.environ.get("FLASK_SECRET_KEY")

# print(os.environ.get("FLASK_SECRET_KEY"))

def get_handle_color(rating):
    if rating<1200:
        return "#36454F"
    elif 1200<=rating<1400:
        return "green"
    elif 1400<=rating<1600:
        return "cyan"
    elif 1600<=rating<1900:
        return "#4169E1"
    elif 1900<=rating<2100:
        return "violet"
    elif 2100<=rating<2400:
        return "orange"
    else:
        return "#D22B2B"
    
def get_atcoder_handle_rank_color(rating):
    color = ""
    rank = ""
    if rating<400:
        color = "#36454F"
    elif 400<=rating<800:
        color = "#E97451"
    elif 800<=rating<1200:
        color = "green"
    elif 1200<=rating<1600:
        color = "cyan"
    elif 1600<=rating<2000:
        color = "blue"
    elif 2000<=rating<2400:
        color = "yellow"
    elif 2400<=rating<2800:
        color = "orange"
    else:
        color = "red"
    
    if rating<2000:
        if rating<400:
            rank = "Unrated"
        else:
            num = (2000-rating)//200 + (rating%200 != 0)
            rank = f"{num} Kyu"
        # print(rank)
    else:
        num = (rating-2000)//200 + 1
        rank = f"{num} Dan"

    return rank, color
    
def get_user_verdict(probs, prob_rating):
    user_verdicts = {}
    correct_cnt = 0
    map_name = f"mapOfProbRating{prob_rating}"
    prob_rating_map = getattr(global_maps, map_name, None)

    if prob_rating_map is None:
        raise ValueError(f"Global dictionary {map_name} does not exist. Check if it was correctly initialized.")

    for prob in probs:
        if "contestId" in prob["problem"]:
            contestIdFull = str(prob["problem"]["contestId"]) + prob["problem"]["index"]
            if contestIdFull in prob_rating_map:
                idx = prob_rating_map[contestIdFull]
                if idx in user_verdicts and user_verdicts[idx] == "AC":
                    continue
                if prob["verdict"] == "OK":
                    user_verdicts[idx] = "AC"
                    correct_cnt += 1
                else:
                    user_verdicts[idx] = "WA"

    return user_verdicts, correct_cnt

def get_user_verdict_atcoder(probs, prob_rating, userhandle):
    user_verdicts = {}
    correct_cnt = 0
    map_name = f"mapOfAtcoderProbRating{prob_rating}"
    prob_rating_map = getattr(global_maps, map_name, None)

    url = API_ATCODER_USER_PROBLEM_STATUS.format(userhandle, 0)
    response = requests.get(url)
    probs = response.json()

    while response.status_code == 200:
        probs = response.json()
        cnt = 0
        for prob in probs:
            cnt = cnt+1
            if "problem_id":
                contestIdFull = prob["problem_id"]
                if contestIdFull in prob_rating_map:
                    idx = prob_rating_map[contestIdFull]
                    if idx in user_verdicts and user_verdicts[idx] == "AC":
                        continue
                    if prob["result"] == "AC":
                        user_verdicts[idx] = "AC"
                        correct_cnt += 1
                    else:
                        user_verdicts[idx] = "WA"
        curTime = probs[-1]["epoch_second"]
        print(curTime)
        # time.sleep(1)
        if cnt<500:
            break
        
        url = API_ATCODER_USER_PROBLEM_STATUS.format(userhandle, curTime+1)
        response = requests.get(url)

    return user_verdicts, correct_cnt

def get_stats_codeforces(probs):
    visited = set()
    tag_frequencies = []
    level_frequencies = []
    problem_rating_frequencies = []
    language_frequency = []
    verdict_frequency = {'AC': 0, 'WA': 0, 'TLE': 0, 'MLE': 0, 'CE': 0, 'RE': 0}
    stats = [0] * 4 #tried, solved, avg attempts, solved with one submission

    for prob in probs["result"]:
        if "contestId" not in prob["problem"]:
            continue
        stats[2] += 1
        if prob["verdict"] == "OK":
            contest_id = prob["problem"]["contestId"]
            index = prob["problem"]["index"]
            verdict_frequency["AC"] += 1
            if (contest_id, index) not in visited:
                visited.add((contest_id, index))
                stats[1] += 1
                level_frequencies.extend(index[0])
                if "rating" in prob["problem"]:
                    rating = prob["problem"]["rating"]
                    if isinstance(rating, list):  # Check if it's iterable
                        problem_rating_frequencies.extend(rating)
                    else:
                        problem_rating_frequencies.append(rating)
                tags = prob["problem"]["tags"]
                tag_frequencies.extend(tags)
                language_frequency.append(prob["programmingLanguage"])
        elif prob["verdict"] == "WRONG_ANSWER":
            verdict_frequency["WA"] += 1
        elif prob["verdict"] == "TIME_LIMIT_EXCEEDED":
            verdict_frequency["TLE"] += 1
        elif prob["verdict"] == "MEMORY_LIMIT_EXCEEDED":
            verdict_frequency["MLE"] += 1
        elif prob["verdict"] == "COMPILATION_ERROR":
            verdict_frequency["CE"] += 1
        elif prob["verdict"] == "RUNTIME_ERROR":
            verdict_frequency["RE"] += 1

    stats[2] /= stats[1]
    # print(type(stats[2]))
    stats[2] = float(f"{stats[2]:.2f}")

    # Count the frequencies of each tag
    lang_counts = Counter(language_frequency)
    tag_counts = Counter(tag_frequencies)
    level_counts = Counter(level_frequencies)
    problem_rating_counts = Counter(problem_rating_frequencies)
    sorted_level_frequencies = sorted(level_counts.items(), key=lambda x: x[0])
    sorted_problem_rating_frequencies = sorted(problem_rating_counts.items(), key=lambda x: x[0])

    return tag_counts, sorted_level_frequencies, sorted_problem_rating_frequencies, stats, lang_counts, verdict_frequency

def get_stats_atcoder(probs):
    visited = set()
    level_frequencies = []
    language_frequency = []
    verdict_frequency = {'AC': 0, 'WA': 0, 'TLE': 0, 'MLE': 0, 'CE': 0, 'RE': 0}
    stats = [0] * 4 #tried, solved, avg attempts, solved with one submission

    for prob in probs:
        if "contest_id" not in prob:
            continue
        stats[2] += 1
        if prob["result"] == "AC":
            problem_id = prob["problem_id"]
            index = problem_id[-1].upper()
            verdict_frequency["AC"] += 1
            if (problem_id) not in visited:
                visited.add((problem_id))
                stats[1] += 1
                if index[0]>='A' and index[0]<='Z':
                    level_frequencies.extend(index[0])
                language_frequency.append(prob["language"])
        elif prob["result"] == "WA":
            verdict_frequency["WA"] += 1
        elif prob["result"] == "TLE":
            verdict_frequency["TLE"] += 1
        elif prob["result"] == "MLE":
            verdict_frequency["MLE"] += 1
        elif prob["result"] == "CE":
            verdict_frequency["CE"] += 1
        elif prob["result"] == "RE":
            verdict_frequency["RE"] += 1

    stats[2] /= stats[1]
    # print(type(stats[2]))
    stats[2] = float(f"{stats[2]:.2f}")

    lang_counts = Counter(language_frequency)
    level_counts = Counter(level_frequencies)
    sorted_level_frequencies = sorted(level_counts.items(), key=lambda x: x[0])

    return sorted_level_frequencies, stats, lang_counts, verdict_frequency

def get_user_info_atcoder(user_infos):
    info = [0] * 7 # #contests, #best_rank, #worst_rank, max_up, max_down, max_rating, current_rating
    info[1] = info[4] = 100000
    info[3] = -10000
    for user_info in user_infos:
        if user_info["IsRated"] == True:
            info[0] = info[0]+1
            info[1] = min(user_info["Place"], info[1])
            info[2] = max(user_info["Place"], info[2])
            info[3] = max(user_info["NewRating"]-user_info["OldRating"], info[3])
            info[4] = min(user_info["NewRating"]-user_info["OldRating"], info[4])
            info[5] = max(info[5], user_info["NewRating"])
            info[6] = user_info["NewRating"]
    return info


def get_user_info_codeforces(user_infos):
    info = [0] * 7 # #contests, #best_rank, #worst_rank, max_up, max_down, max_rating, current_rating
    info[1] = info[4] = 100000
    info[3] = -10000
    for user_info in user_infos:
        info[0] = info[0]+1
        info[1] = min(user_info["rank"], info[1])
        info[2] = max(user_info["rank"], info[2])
        info[3] = max(user_info["newRating"]-user_info["oldRating"], info[3])
        info[4] = min(user_info["newRating"]-user_info["oldRating"], info[4])
        info[5] = max(info[5], user_info["newRating"])
        info[6] = user_info["newRating"]
    return info

def find_max_and_cur_rating_Atcoder(data):
    max_rating = max(result['NewRating'] for result in data)
    cur_rating = data[-1]['NewRating']
    return max_rating, cur_rating

def get_visit_count():
    if os.path.exists("visit_count.txt"):
        with open("visit_count.txt", "r") as file:
            return int(file.read())
    else:
        return 0

def update_visit_count(visit_count):
    with open("visit_count.txt", "w") as file:
        file.write(str(visit_count))

def get_slide_num(prob_rating):
    if prob_rating<=1700:
        return 0
    elif prob_rating<=2700:
        return 1
    return 2

def get_slide_num_atcoder(prob_rating):
    if prob_rating<=1400:
        return 0
    elif prob_rating<=2800:
        return 1
    return 2

@app.route("/")
def home():

    visit_count = get_visit_count()
    visit_count += 1
    # Update the visit count in the persistent storage
    update_visit_count(visit_count)

    return render_template("home.html", visit_count=visit_count)

@app.route("/codeforces", methods=['POST', 'GET'])
def codeforces():
    visit_count = get_visit_count()
    visit_count += 1
    update_visit_count(visit_count)

    userhandle = request.form.get('userhandle', '')  # Get userhandle from form data
    prob_rating = request.form.get('rating')
    
    with open(f'cf-problem-tags/tags.json', 'r') as f:
        tags = json.load(f)

    if request.method == "POST" and userhandle:
        url = API_CODEFORCES_USER_INFO.format(userhandle)
        response = requests.get(url)
        # Parse JSON response
        data = response.json()
        
        # Check if API response is successful
        if data.get("status") == "OK":
            # Accessing rank, maxRating, and rating
            if "rank" in data["result"][0]:
                rank = data["result"][0]["rank"]
                max_rating = data["result"][0]["maxRating"]
                rating = data["result"][0]["rating"]
                ratingColor = get_handle_color(rating)
            else:
                rank = "Unrated"
                rating = 0
                max_rating = 0
                ratingColor = get_handle_color(rating)

            url = API_CODEFORCES_USER_PROBLEM_STATUS.format(userhandle)
            response = requests.get(url)
            probs = response.json()

            if prob_rating != None:
                list_rating = prob_rating
            else:
                list_rating = min(max(800, (rating - rating%100)+200), 3500)
                prob_rating = list_rating

            with open(f'cf-rating-problems/{list_rating}.json', 'r') as f:
                problems = json.load(f)

            correct_cnt = 0
            user_verdicts, correct_cnt = get_user_verdict(probs["result"], list_rating)

            prob_rating = int(prob_rating)
            slide_num = get_slide_num(prob_rating)
            
            # Render the template with userhandle included
            return render_template("codeforces.html", userhandle=userhandle, rank=rank, max_rating=max_rating, 
                                   rating=rating, problems=problems, tags=tags['tags'], probs=probs["result"], 
                                   ratingColor=ratingColor, user_verdicts=user_verdicts, correct_cnt=correct_cnt, 
                                   visit_count=visit_count, prob_rating=prob_rating, slide_num=slide_num)
    
    if prob_rating==None:
        prob_rating = 1500

    with open(f'cf-rating-problems/{prob_rating}.json', 'r') as f:
        problems = json.load(f)
    
    prob_rating = int(prob_rating)

    slide_num = get_slide_num(prob_rating)

    # Render the template with userhandle unchanged
    return render_template("codeforces.html", userhandle='', problems=problems, tags=tags['tags'], correct_cnt=0, 
                           user_verdicts={}, visit_count=visit_count, prob_rating=prob_rating, slide_num=slide_num)



@app.route("/atcoder", methods=['POST', 'GET'])
def atcoder():
    visit_count = get_visit_count()
    visit_count += 1
    # Update the visit count in the persistent storage
    update_visit_count(visit_count)

    userhandle = request.form.get('userhandle', '')  # Get userhandle from form data
    prob_rating = request.form.get('rating')

    if request.method == "POST" and userhandle:
        url = API_ATCODER_USER_CONTEST_INFO.format(userhandle)
        response = requests.get(url)
  
        # Check if API response is successful
        if response.status_code == 200:
            data = response.json()

            max_rating, rating = find_max_and_cur_rating_Atcoder(data)
            # print("HEllo")

            url = API_ATCODER_USER_PROBLEM_STATUS.format(userhandle, 0)
            response = requests.get(url)
            probs = response.json()

            rank, ratingColor = get_atcoder_handle_rank_color(rating)
            user_rating = min(3800, max(0, (rating - rating%200)+200))
            if prob_rating:
                user_rating = prob_rating
            else:
                prob_rating = user_rating
            prob_rating = int(prob_rating)
            slide_num = get_slide_num_atcoder(prob_rating)

            with open(f'atcoder-rating-problems/{user_rating}.json', 'r') as f:
                problems = json.load(f)

            correct_cnt = 0
            user_verdicts, correct_cnt = get_user_verdict_atcoder(probs, prob_rating, userhandle)

            return render_template("atcoder.html", userhandle=userhandle, prob_rating=prob_rating, rank=rank, 
                                   ratingColor=ratingColor, visit_count=visit_count, max_rating=max_rating, rating=rating, problems=problems,
                                   slide_num=slide_num, user_verdicts=user_verdicts, correct_cnt=correct_cnt)
    user_rating = 600
    if prob_rating:
        user_rating = prob_rating
    else:
        prob_rating = user_rating 
    prob_rating = int(prob_rating)

    slide_num = get_slide_num_atcoder(prob_rating)
    
    with open(f'atcoder-rating-problems/{user_rating}.json', 'r') as f:
        problems = json.load(f)
    return render_template("atcoder.html", userhandle='', prob_rating=prob_rating, problems=problems, user_verdicts={}, visit_count=visit_count, correct_cnt=0, slide_num=slide_num)


@app.route("/codechef", methods=['POST', 'GET'])
def codechef():
    visit_count = get_visit_count()
    # visit_count += 1
    # Update the visit count in the persistent storage
    # update_visit_count(visit_count)

    return render_template("codechef.html", visit_count=visit_count)


@app.route("/codeforces-visualizer", methods=['POST', 'GET'])
def cfvisualizer():
    visit_count = get_visit_count()
    visit_count += 1
    # Update the visit count in the persistent storage
    update_visit_count(visit_count)

    userhandle = request.form.get('userhandle', '')  # Get userhandle from form data

    if request.method == "POST" and userhandle:
        url = API_CODEFORCES_USER_INFO.format(userhandle)
        response = requests.get(url)
        # Parse JSON response
        data = response.json()
        
        # Check if API response is successful
        if data.get("status") == "OK":
            url = API_CODEFORCES_USER_PROBLEM_STATUS.format(userhandle)
            response = requests.get(url)
            probs = response.json()
            
            tag_frequencies, level_frequencies, rating_frequencies, stats, lang_counts, verdict_counts = get_stats_codeforces(probs)

            url = API_CODEFORCES_USER_CONTEST_INFO.format(userhandle)
            response = requests.get(url)
            user_infos = response.json()

            info = get_user_info_codeforces(user_infos["result"])

            # for lang, count in lang_counts:
            #     print(f"Language: {lang}, Count: {count}")

            return render_template("codeforces-visualizer.html", userhandle=userhandle, lang_counts=lang_counts, verdict_counts=verdict_counts, stats=stats, info=info, tag_frequencies=tag_frequencies, level_frequencies=level_frequencies, rating_frequencies=rating_frequencies, visit_count=visit_count)

    return render_template("codeforces-visualizer.html", userhandle='', visit_count=visit_count)

@app.route("/atcoder-visualizer", methods=['POST', 'GET'])
def atcvisualizer():
    visit_count = get_visit_count()
    visit_count += 1
    # Update the visit count in the persistent storage
    update_visit_count(visit_count)

    userhandle = request.form.get('userhandle', '')  # Get userhandle from form data

    if request.method == "POST" and userhandle:
        url = API_ATCODER_USER_CONTEST_INFO.format(userhandle)
        response = requests.get(url)
        user_infos = response.json()
        
        # Check if API response is successful
        if response.status_code == 200:
            url = API_ATCODER_USER_PROBLEM_STATUS.format(userhandle, 0)
            response = requests.get(url)
            probs = response.json()
            
            level_frequencies, stats, lang_counts, verdict_counts = get_stats_atcoder(probs)

            info = get_user_info_atcoder(user_infos)

            return render_template("atcoder-visualizer.html", userhandle=userhandle, lang_counts=lang_counts, verdict_counts=verdict_counts, stats=stats, info=info, level_frequencies=level_frequencies, visit_count=visit_count)

    return render_template("atcoder-visualizer.html", userhandle='', visit_count=visit_count)

@app.route('/your-flask-endpoint', methods=['POST'])
def receive_selected_tags():
    data = request.json
    selected_tags = data.get('selectedTags')
    # Process selected tags as needed
    print(selected_tags)
    return jsonify({'message': 'Selected tags received successfully'})

app.run(debug=True, host='0.0.0.0', port='5000')