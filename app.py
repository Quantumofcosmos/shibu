import os
from flask_session import Session
from flask import Flask, render_template, abort, request, session, app
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import time 
import datetime

keeper = time.time()
keeper0 = time.time()

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = 'secretkey00'
Session(app)

app = Flask(__name__)

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
mentionflag=0
msgflag=0
ip_ban_list = ['103.224.182.212']


@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=60)
    try:
        ip = request.remote_addr
    except:
        ip = ['999.999.999.999']
    
    if ip in ip_ban_list:
        abort(403)

@app.route("/", methods=["GET", "POST"])
def index():
     try:
        if session['value'] is None:
            
            print(0)
        
       
    except:
    
        session['value']=0
    
    status=0
    if request.method == "POST":
        msg= request.form.get("name")
        if session['value'] >= 3:
            status=6
            return render_template("index.html", status=status)
            
        session['value'] += 1
        

        if "@" in msg:
            mentionflag += 1

        if mentionflag == 5:
            keeper=time.time()

        if mentionflag >= 5:
            keeper2 = time.time()
            diff = keeper2 - keeper
            if diff > 1800:
                mentionflag=0
            if mentionflag = 0:
                print('awoken')

        if mentionflag >=5:
            status=5
            return render_template("index.html", status=status)
            

            
        
        if "https://" in msg:
            status=2
            return render_template("index.html", status=status)
      
            
        msgflag += 1

        if msgflag ==15:
            keeper0 = time.time()
            
        
        if msgflag >= 15:
            
            keeper3 = time.time()
            diff2 = keeper3 - keeper0
            if diff2 > 1800:
                msgflag=0
            if msgflag = 0:
                print('awoken')

        if msgflag >= 15:
            status=10
            return render_template("index.html", status=status)


        
            
        
        if msg is "":
            status=2
            return render_template("index.html", status=status)
        db.execute("INSERT INTO operation (msg) VALUES (:msg)",
                {"msg": msg})
        db.commit()
        status=1

    return render_template("index.html", status=status)
