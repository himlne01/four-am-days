import psycopg2
import os
from flask import Flask, make_response, redirect, render_template, request, url_for

app = Flask(__name__)
SECRET_KEY = os.environ.get("SECRET_KEY")

def get_data_from_db(query: str) -> list:
    conn = psycopg2.connect(
        database = "dgju4sm6llfrr",
        user="tlcqqkcatmpplu",
        password=SECRET_KEY,
        host="ec2-34-200-72-77.compute-1.amazonaws.com",
        port="5432"
    )
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    return rows

@app.route("/")
def index():
    if request.method == "GET":
        return render_template("index.html")


@app.route("/blog/<string:theDate>")
def journal(theDate):
    print(theDate)
    # query_words = "SELECT * FROM wordofday WHERE date = '" + theDate + "';"
    # query_journal = "SELECT * FROM journaling WHERE date = '" + theDate + "';"
    # query_rbt = "SELECT * FROM flowers WHERE date = '" + theDate + "';"
    # big={'words': get_data_from_db(query_words),'journal':get_data_from_db(query_journal), 'rbt':get_data_from_db(query_rbt)}
    return render_template("/base.html") #, specs=big) 


@app.route("/search", methods=["POST"])
def search():
    # LOOK THROUGH THE THEMES OF THE DATABASE
    searching_for = request.form.get("searchith")
    date_data = get_data_from_db("SELECT date FROM journaling WHERE themes LIKE '%"+searching_for+"%';")
    if date_data != []:
        return render_template("search.html", options=date_data)
    else:
        return render_template("search.html", options=[[("This theme is not in use")]])
