from flask import Flask, request, redirect, render_template, flash, session, render_template_string
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy

import json
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
    return render_template("base.html")




app.run(debug=True)