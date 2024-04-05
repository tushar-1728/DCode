from flask import Flask, request, redirect, render_template, flash, render_template_string
from flask.helpers import url_for

import os
import json, requests

app = Flask("DCODE")
app.secret_key = "divyaraj"

def getHandleColor(rating):
    if rating<1200:
        return "gray"
    elif 1200<=rating<1400:
        return "green"
    elif 1400<=rating<1600:
        return "cyan"
    elif 1600<=rating<1900:
        return "blue"
    elif 1900<=rating<2100:
        return "violet"
    elif 2100<=rating<2300:
        return "orange"
    elif 2300<=rating<2400:
        return "orange"
    elif 2400<=rating<2600:
        return "red"
    elif 2600<=rating<3000:
        return "red"
    else:
        return "red"
    
def user__Verdict(probs, problems):
    user_verdicts = {}
    key_counter = 1
    correct_cnt = 0

    for problem in problems:
        verdict = "NA"
        for prob in probs:
            if prob["problem"]["contestId"] == problem["contestId"] and prob["problem"]["index"] == problem["index"]:
                if prob["verdict"] == "OK":
                    verdict = "AC"
                    correct_cnt += 1
                    break
                else:
                    verdict = "WA"

        user_verdicts[key_counter] = verdict
        key_counter += 1

    return user_verdicts, correct_cnt

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/codeforces", methods=['POST', 'GET'])
def codeforces():
    userhandle = request.form.get('userhandle', '')  # Get userhandle from form data
    user_rating = 1500
    with open(f'cf-rating-problems/{user_rating}.json', 'r') as f:
        problems = json.load(f)[:100]  # Load the first hundred problems
    
    with open(f'cf-problem-tags/tags.json', 'r') as f:
        tags = json.load(f)

    if request.method == "POST" and userhandle:
        url = f"https://codeforces.com/api/user.info?handles={userhandle}&checkHistoricHandles=false"
        response = requests.get(url)
        # Parse JSON response
        data = response.json()
        
        # Check if API response is successful
        if data.get("status") == "OK":
            # Accessing rank, maxRating, and rating
            rank = data["result"][0]["rank"]
            max_rating = data["result"][0]["maxRating"]
            rating = data["result"][0]["rating"]
            ratingColor = getHandleColor(rating)

            url = f"https://codeforces.com/api/user.status?handle={userhandle}&from=1&count=9999"
            response = requests.get(url)
            probs = response.json()

            # user_rating = 1700
            list_rating = min(max(800, (rating - rating%100)+200), 3500)

            with open(f'cf-rating-problems/{list_rating}.json', 'r') as f:
                problems = json.load(f)[:100]  # Load the first hundred problems

            correct_cnt = 0
            user_verdicts, correct_cnt = user__Verdict(probs["result"], problems)
            for verdict in user_verdicts:
                print(user_verdicts[verdict])
            
            # Render the template with userhandle included
            return render_template("codeforces.html", userhandle=userhandle, rank=rank, max_rating=max_rating, rating=rating, problems=problems, tags=tags['tags'], probs=probs["result"], ratingColor=ratingColor, user_verdicts=user_verdicts, correct_cnt=correct_cnt)
    # Render the template with userhandle unchanged
    return render_template("codeforces.html", userhandle=userhandle, problems=problems, tags=tags['tags'])



@app.route("/atcoder", methods=['POST', 'GET'])
def atcoder():
    return render_template("atcoder.html")


@app.route("/codechef", methods=['POST', 'GET'])
def codechef():
    return render_template("codechef.html")

app.run(debug=True)