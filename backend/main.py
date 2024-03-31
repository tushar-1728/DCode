from flask import Flask, request, redirect, render_template, flash, session, render_template_string
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy

import json, requests
from flask_mail import Mail, Message

#my database connection
# local_server = True
app = Flask(__name__)
app.secret_key = "divyaraj"

# with open('config.json', 'r') as c:
#     params = json.load(c)["params"]

# app.config.update(
#     MAIL_SERVER = 'smtp.gmail.com',
#     MAIL_PORT = '465',
#     MAIL_USE_SSL = True,
#     MAIL_USERNAME = params['gmail-user'],
#     MAIL_PASSWORD = params['gmail-pswd']
# )
# mail = Mail(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/databsename'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/covid'
# db = SQLAlchemy(app)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/codeforces", methods=['POST', 'GET'])
def codeforces():
    userhandle = request.form.get('userhandle', '')  # Get userhandle from form data
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
            
            # Render the template with userhandle included
            return render_template("codeforces.html", userhandle=userhandle, rank=rank, max_rating=max_rating, rating=rating)
        return render_template("codeforces.html", userhandle='')
    # Render the template with userhandle unchanged
    return render_template("codeforces.html", userhandle=userhandle)



app.run(debug=True)