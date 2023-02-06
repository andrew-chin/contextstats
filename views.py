from flask import Blueprint, render_template
import pandas as pd

df = pd.read_csv('players.csv', delimiter=',')
dicts = df.to_dict().values()


views = Blueprint(__name__, "views")

@views.route("/")
def home():
    return render_template("home.html")
