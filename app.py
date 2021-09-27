import os

from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
recent = ["", "", "", "", ""]
#lol
@app.route("/", methods=["GET", "POST"])
def index():
    status=0
    realflag=False
    if request.method == "POST":
        msg= request.form.get("name")
        if msg is None:
            status=2
            return render_template("index.html", status=status)
        count=0
        while count < 5:
            flag = recent[count] in msg
            if flag:
                realflag=True
            count += 1
        if realflag:
            status=2
            return render_template("index.html", status=status)
        recent.extend(msg)
        recent.pop(0)
        db.execute("INSERT INTO operation (msg) VALUES (:msg)",
                {"msg": msg})
        db.commit()
        status=1

    return render_template("index.html", status=status)
