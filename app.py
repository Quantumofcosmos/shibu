import os
import csv
from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

ipbanlist=[]
f=open("bannedips.csv")
reader= csv.reader(f)
for bip in reader:
    
    ipbanlist.extend(bip)






@app.route("/", methods=["GET", "POST"])
def index():
    msgip = request.remote_addr
    if msgip in ipbanlist:
      realflag=True
    status=0
    if request.method == "POST":
        msg= request.form.get("name")
        if msg is None:
            status=2
            return render_template("index.html", status=status)
        realflag=False
        s="https://"
        realflag= s in msg
        
            
      
        if realflag:
            status=2
            realflag=False
            return render_template("index.html", status=status)
        db.execute("INSERT INTO operation (msg) VALUES (:msg)",
                {"msg": msg})
        db.commit()
        status=1

    return render_template("index.html", status=status)
