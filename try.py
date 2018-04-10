import os
import json
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'some_secret'

user = {"username":"",
        "score" : 0 }

def write_to_file(filename, data):
    with open(filename, "a") as file:
        file.writelines(data)

def add_to_scoreboard(username, score):
    write_to_file('data/scoreboard.txt', "{0} {1} - {2}\n".format(
            score,
            username.title(),
            datetime.now().strftime("%d/%m/%y - %H:%M:%S")))
            
def display_scoreboard():
    scoreboard = []
    with open('data/scoreboard.txt', 'r') as score_data:
        scoreboard = score_data.readlines()
    ordered = sorted(scoreboard, key= (lambda line: int(line.lstrip().split(' ')[0])))
    return ordered

@app.route('/', methods = ["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        user['username'] = username
        return redirect('/1')
    return render_template("index.html")
    

@app.route('/<number>', methods=["GET", "POST"])
def get_info(number):
    riddle = {}
    with open("data/riddle_data.json", "r") as json_data:
        data = json.load(json_data)
        for obj in data:
            if obj["url"] == number:
                riddle = obj
  
    return render_template("member.html", riddle=riddle, user=user)


@app.route('/submit_answer', methods = ["POST"])
def check_answer():
    if request.method == 'POST':
        url = int(request.form["url"])
        guess = request.form['answer'].title()
        answer = request.form["solution"]
        if url < 10:
            
            if guess == answer:
                url += 1
                user['score'] += 1
                return redirect(url)
            elif guess == "Pass":
                url += 1
                return redirect(url)
            else:
                flash("{} is incorrect. Please try again".format(guess))
                return redirect(url)
        else:
            add_to_scoreboard(user['username'], user['score'])
            return redirect('leaderboard')
            
 
@app.route('/leaderboard')
def leaderboard():
    scoreboard = display_scoreboard()
    return render_template("leaderboard.html", scoreboard=scoreboard)
    


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug = True)  