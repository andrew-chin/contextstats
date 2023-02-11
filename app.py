import csv
from flask import Flask, render_template, request, send_file, Response
import io
import re
from matplotlib.pyplot import bar_label
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import math
from math import pi
from urllib.parse import urlencode


app = Flask(__name__)

def find_name(url):
    splits = url.split('/')

    name = splits[-1].replace("-Scouting-Report", "")

    full_name = name.replace("-", " ")

    return(full_name)

def is_valid_fbref_url(url):
    regex = re.compile(
        r'^https://fbref.com/en/players/[a-zA-Z0-9]+/scout/365_m1/[a-zA-Z0-9-]+-Scouting-Report$')

    return re.match(regex, url) is not None
 
def compare_player_data(x, y):
    titles = []
    values = []
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
                    titles.append(x[1])
                    values.append([x_float, y_float, x[1]])
            except:
                continue
    return [titles, values]

def get_player_data(x):
    table_data = []
    df = pd.read_html(x, flavor='html5lib')
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


@app.route("/index")
def index():
    return render_template(index = data)

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
    url1 = 0
    url2 = 0

    if(is_valid_fbref_url(data1)):
        data1 = data1
        url1 = 1
        name1 = find_name(data1)
    else:
         data1 = search_csv_fbref(data1)
         name1 = search_csv_name(data1)
    if(is_valid_fbref_url(data2)):
        data2 = data2
        url2 = 1
        name2 = find_name(data2)
    else:
        data2 = search_csv_fbref(data2)
        name2 = search_csv_name(data2)
        
 
    p1 = get_player_data(data1)
    p2 = get_player_data(data2)
    fin = compare_player_data(p1, p2)
    titles = fin[0]
    values = fin[1]
    rows = len(fin[1])
    if(url1 == 1 and url2 == 1):
        text = "Wow. You weren't wrong,  " + name1 + " is clearly a way better player than " + name2 + "!"
    if(url1 == 0 and url2 == 0):
        text = "Wow. You weren't wrong,  " + search_csv_name(data1) + " is clearly a way better player than " + search_csv_name(data2) + "!"
    if(url1 == 0 and url2 == 1):
        text = "Wow. You weren't wrong,  " + search_csv_name(data1) + " is clearly a way better player than " + name2 + "!"
    if(url1 == 1 and url2 == 0):
        text = "Wow. You weren't wrong,  " + name1 + " is clearly a way better player than " + search_csv_name(data2) + "!"
    
    return render_template("home.html", rows = rows, text = text, titles = titles, values = values, data = read_csv('players.csv'), name1=name1,name2=name2 )

    

if __name__ == '__main__':
    app.run(debug=True)

