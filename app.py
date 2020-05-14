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
    query_words = "SELECT * FROM wordofday WHERE date = '" + theDate + "';"
    query_journal = "SELECT * FROM journaling WHERE date = '" + theDate + "';"
    query_rbt = "SELECT * FROM flowers WHERE date = '" + theDate + "';"
    big={'words': get_data_from_db(query_words),'journal':get_data_from_db(query_journal), 'rbt':get_data_from_db(query_rbt)}
    # if theDate == '06-01':
    #     big={"words":('06-01', '??', 'riji (say r like "grr" and "jeep" without the "p")', 'Diary'),"journal":('06-01', 'Sunrise', 'beginning\\nintention', 'Did I start writing on the twenty-eighth of May? Yes, I did.\\nI wanted to start off my ?? by reflecting a little bit on the past school year. I am half done with my undergrad schooling. I have half left to go. Something tells me I am currently in "the good ole days," but from April and May, I do not think I would have agreed with you.\\n"Intention" is one of the key words of the year. You know when you know a piece of information but it take a while for you to truly connect the meaning of the word to something relatable in your life? When you make any form of connection, it more or less hits you like a bus. Putting your energy, strength, and heart into a series of actions or a goal is very powerful. The saying is true: you can get a lot done when you put your mind to it.\\nThe main reason I connected with the word "Intention" is through Ultimate Frisbee. If I ferociously put my mind into doing one thing at a time, I actually play better. /Who would have thought?/ Some people may get confused with the word "Intense" which means playing with competitive ferociousness. No. I mean another word for focus. But you can focus on anything; you can focus on distractions. With "Intention," you put the focus on your goal.'),"rbt":('06-01', 'Lacking sleep', 'The Calendar Layout with tables!', 'More updates')}
    # elif theDate == '06-12':
    #     big = {"words":('06-12', '???', 'bu mai che (say "boo", "my", "chug" without the "g")', 'To not buy a car'),"journal":('06-12', '"Anything but the Corolla"', 'transportation\\ntime', 'If Shakespeare was alive today as a young, Chinese person with my problem, he would maybe say, "?? or ???". (He would not ask it though because I haven’t explained the how to do the questioning.)\\nI am more or less patiently waiting for an answer. To live in the city with public transportation and my bike? Or to live in a smaller town and make the big purchase? Would I even drive it enough to make up for the enormous increase in my carbon footprint?\\nAlso, if being patient means that a person can wait longer, does that mean the person has a different perception of time than others? Hmmm, a question for my physics/philosophy major of a sister. Haha, please don’t ask me about her plans. :)'),"rbt":('06-12', 'Transportation purchases are expensive', 'I am feeling patient right now.', 'City living')}
    # print(big['words'][0])
    print(big['journal'][0])
    # print(big['rbt'][0])
    return render_template("/blog.html", specs=big) 


@app.route("/search", methods=["POST"])
def search():
    # LOOK THROUGH THE THEMES OF THE DATABASE
    searching_for = request.form.get("searchith")
    date_data = get_data_from_db("SELECT date FROM journaling WHERE themes LIKE '%"+searching_for+"%';")
    if date_data != []:
        return render_template("search.html", options=date_data)
    else:
        return render_template("search.html", options=[[("This theme is not in use")]])
