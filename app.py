import csv
import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)

df = pd.read_html('https://fbref.com/en/players/d70ce98e/scout/365_m1/Lionel-Messi-Scouting-Report', flavor='html5lib')
table_data = []
for idx, table in enumerate(df):
    if idx == 5:
        table_data.append("<h3>Table {}</h3>".format(idx))
        table_data.append(table.to_html())

result = "\n".join(table_data)



def read_csv(filename):
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        return list(reader)



@app.route("/")
def home():
    data = read_csv('players.csv')
    return render_template("home.html", data=data, table=result)


@app.route("/submit", methods=['POST'])
def submit():
    name = request.form['name']
  
    

if __name__ == '__main__':
    app.run(debug=True)

