import os

from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import time 
app = Flask(__name__)

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
check=False
count=0
keeper=0
@app.route("/", methods=["GET", "POST"])
def index():
    keeper2 = time.time()
    status=0
    if request.method == "POST":
        msg= request.form.get("name")

        
        diff= keeper2 - keeper
        
        
        
        if "https://" in msg:
            status=2
            return render_template("index.html", status=status)
        
        if "@" in msg:
                        
            if count >= 6:
                if check:
                    if diff > 1800:
                        
                        count=0
                        check=False
                    
                    
                status=5
                
                return render_template("index.html", status=status)

            else:
                count += 1
                if count == 6:
                    check=True
                    keeper = time.time()
                    
                
            
      
            
            
        
        if msg is None:
            status=2
            return render_template("index.html", status=status)
        db.execute("INSERT INTO operation (msg) VALUES (:msg)",
                {"msg": msg})
        db.commit()
        status=1

    return render_template("index.html", status=status)
