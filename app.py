"""
File:        main.py
Author:      Ian Kollipara
Created:     2026-02-23
Description: Simple Flask App for taking Attendence
"""

import flask
import flask_wtf
import wtforms
from wtforms import validators
from datetime import datetime
from zoneinfo import ZoneInfo
import csv


class AttendenceForm(flask_wtf.FlaskForm):
    name = wtforms.StringField(
        "Name", validators=[validators.DataRequired("You must give a name")]
    )
    date = wtforms.DateTimeLocalField()


app = flask.Flask(__name__)
app.config["SECRET_KEY"] = "bus371"
_ = flask_wtf.CSRFProtect(app)


@app.route("/", methods=["GET", "POST"])
def index():
    form = AttendenceForm(data={"date": datetime.now(ZoneInfo("America/Chicago"))})
    if form.validate_on_submit():
        name = form.data["name"]
        date = form.data["date"]
        with open("./attendence.csv", "a+") as f:
            w = csv.DictWriter(f, ["Name", "Date"])
            w.writerow({"Name": name, "Date": date})

        return flask.render_template("success.html")

    return flask.render_template("index.html", form=form)
