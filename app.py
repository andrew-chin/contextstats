import csv
import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)


def read_csv(filename):
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        return list(reader)


@app.route("/")
def home():
    data = read_csv('players.csv')
    return render_template("home.html", data=data)


@app.route("/submit", methods=['POST'])
def submit():
    name = request.form['name']
    # Use the name value to perform desired actions
    # ...
    

if __name__ == '__main__':
    app.run(debug=True, port=8000)

