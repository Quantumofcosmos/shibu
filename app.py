import os

from flask import Flask, render_template, request, g, session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
recent = ["", "", "", "", ""]
#lol
@app.route("/", methods=["GET", "POST"])
def index():
    session['status'] = 0
    session['realflag'] = False
    if request.method == "POST":
        session['msg']= request.form.get("name")
        if msg is None:
            session['status']=2
            return render_template("index.html", status=session['status'])
        session['count']=0
        while session['count'] < 5:
            flag = recent[session['count']] in msg
            if flag:
                session['realflag']=True
            session['count'] += 1
        if session['realflag']:
            session['status']=2
            return render_template("index.html", status=session['status'])
        recent.extend(session['msg'])
        recent.pop(0)
        db.execute("INSERT INTO operation (msg) VALUES (:msg)",
                {"msg": session['msg']})
        db.commit()
        session['status']=1

    return render_template("index.html", status=session['status'])
