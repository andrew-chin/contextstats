import csv
from flask import Flask, render_template, request
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import math
from math import pi
from urllib.parse import urlencode


app = Flask(__name__)


 
def compare_player_data(x, y):
    result = []
    list1 = x.split("\n")
    list2 = y.split("\n")
    for i in range(len(list1)):
        x = list1[i].split(",")
        y = list2[i].split(",")
        
        for j in range(len(x)-1):
            if x[j] == '' or y[j] == '':
                continue
            try:
                x_float = float(x[j])
                y_float = float(y[j])
                if math.isnan(x_float) or math.isnan(y_float):
                    continue
                if x_float > y_float:
                    result.append([x[1], x_float, y_float])
            except:
                continue
    df = pd.DataFrame(result, columns=["Statistic", list1[0], list2[0]])
    fintable = df.to_html()
    return fintable

                 
    df = pd.DataFrame(result, columns=["Statistic", list1[0], list2[0]])
    fintable = df.to_html()
    return fintable

def get_player_data(x):
    table_data = []
    df = pd.read_html(x, flavor='html5lib')
    table_data.append(search_csv_name(x))
    for idx, table in enumerate(df):
        if table.shape[0] >= 110:
            table_data.append(table.to_csv())
            break
    result = "\n".join(table_data)
    return result
    



def search_csv_fbref(name):
    with open('players.csv', 'r') as file:
        reader = csv.reader(file)
        headers = [header.strip() for header in next(reader)]
        name_index = headers.index("Name")
        fbref_index = headers.index("fbref")
        for row in reader:
            if row[name_index].strip() == name:
                return row[fbref_index]
    return None

def search_csv_name(fbref):
    with open('players.csv', 'r') as file:
        reader = csv.reader(file)
        headers = [header.strip() for header in next(reader)]
        name_index = headers.index("Name")
        fbref_index = headers.index("fbref")
        for row in reader:
            if row[fbref_index].strip() == fbref:
                return row[name_index]
    return None


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
    data1 = search_csv_fbref(data1)
    data2 = search_csv_fbref(data2)
    p1 = get_player_data(data1)
    p2 = get_player_data(data2)
    fin = compare_player_data(p1, p2)
    return render_template("home.html", fin = fin, data = read_csv('players.csv'), table1=get_player_data(data1),table2=get_player_data(data2) )

    

if __name__ == '__main__':
    app.run(debug=True)

