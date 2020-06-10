import psycopg2
import os
from flask import Flask, render_template, request
import sqlite3
# from pexels_api import API

app = Flask(__name__)
SECRET_KEY = os.environ.get("SECRET_KEY")
# PEXELS_API_KEY = os.environ.get('YOUR_API_KEY')

# def getPhoto(query: str):
#     api = API(PEXELS_API_KEY)
#     api.search(query, page=12, results_per_page=1)
#     photos = api.get_entries()
#     for photo in photos:
#         return(photo.small)

def get_data_from_db(query: str) -> list:
    conn = sqlite3.connect('day_tabase.sqlite3')

    # conn = psycopg2.connect(
    #     database = "dgju4sm6llfrr",
    #     user="tlcqqkcatmpplu",
    #     password=SECRET_KEY,
    #     host="ec2-34-200-72-77.compute-1.amazonaws.com",
    #     port="5432"
    # )
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    return rows

@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")  
    else:  
        theCategory = request.form.get("category")
        searching_for = request.form.get("searchith")
        if theCategory == 'themes':
            date_data = get_data_from_db("SELECT date FROM journaling WHERE themes LIKE '%"+searching_for+"%';")
        elif theCategory == 'titles':
            date_data = get_data_from_db("SELECT date FROM journaling WHERE title LIKE '%"+searching_for+"%';")
        elif theCategory == 'entry':
            date_data = get_data_from_db("SELECT date FROM journaling WHERE paragraph LIKE '%"+searching_for+"%';")

        if date_data != []:
            return render_template("search.html", options=date_data)
        else:
            return render_template("search.html", options=[[("This theme is not in use")]])


@app.route("/blog/<string:theDate>", methods=["GET"])
def journal(theDate):
    if request.method == "GET":
        query_words = "SELECT * FROM wordofday WHERE date = '" + theDate + "';"
        query_journal = "SELECT * FROM journaling WHERE date = '" + theDate + "';"
        query_rbt = "SELECT * FROM flowers WHERE date = '" + theDate + "';"

        # return render_template("blog.html", words=get_data_from_db(query_words), journal=get_data_from_db(query_journal), rbt=get_data_from_db(query_rbt)) 
        big={'words': get_data_from_db(query_words),'journal':get_data_from_db(query_journal), 'rbt':get_data_from_db(query_rbt)} #, 'thorn': getPhoto('thorn'), 'rose':getPhoto('rose'),'bud':getPhoto('bud')}
        return render_template("blog.html", specs=big) 