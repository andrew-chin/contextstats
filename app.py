import csv
from flask import Flask, render_template
from views import views

app = Flask(__name__)

def read_csv(filename):
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        return list(reader)

@app.route("/")
def home():
    data = read_csv('players.csv')
    return render_template("home.html", data=data)

if __name__ == '__main__':
    app.run(debug=True, port=8000)

