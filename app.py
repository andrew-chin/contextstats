import csv
from flask import Flask, render_template, request
import requests
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import matplotlib as mpl
import warnings
import numpy as np
from math import pi
from urllib.parse import urlencode


app = Flask(__name__)


 

def get_player_data(x):
    table_data = []
    df = pd.read_html(x, flavor='html5lib')
    for idx, table in enumerate(df):
        if idx == 5:
            table_data.append("<h3>Table {}</h3>".format(idx))
            table_data.append(table.to_html())
    result = "\n".join(table_data)
    return result
    







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
  

@app.route('/send_data', methods=['POST'])
def send_data():
    data1 = request.form['data1']
    data2 = request.form['data2']
    return render_template("home.html", data = read_csv('players.csv'), table1=get_player_data(data1),table2=get_player_data(data2) )

    

if __name__ == '__main__':
    app.run(debug=True)

