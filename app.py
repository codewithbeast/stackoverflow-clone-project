from flask import Flask , render_template , redirect , request , session
from werkzeug.security import generate_password_hash,check_password_hash
from flask_session import Session
from cs50 import SQL
from functions import *


app = Flask(__name__)


app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///users.db")

@app.route("/")
def index():
    user = session.get("user_id")
    if user:
        return render_template("index.html")
    
    else:
        return redirect("/login")
    
@app.route("/login",methods=["GET","POST"])
def login():
    
    if request.method == "GET":
        return render_template("login.html")
    
    else:
        if not request.form.get("username"):
            return "<h1> Username not provided ): </h1>"
        
        elif not request.form.get("password"):
            return "<h1> Password not provided ): </h1>"
        



        username = request.form.get("username")
        data = db.execute("SELECT * FROM users WHERE username = ?", username)

        if len(data) !=1 or not check_password_hash(data[0]["hash"],request.form.get("password")):
            return "<h1 Invalid Username/Password </h1>"
        

        session["user_id"] = data[0]["id"]

        return redirect("/")
    
@app.route("/register",methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    

    else:
        if not request.form.get("username"):
            return "<h1> Username not provided ): </h1>"
        
        elif not request.form.get("password"):
            return "<h1> Password not provided ): </h1>"
        
        elif not request.form.get("confirm_password"):
            return "<h1> Password Confirmation not provided ): </h1>"
        
        elif request.form.get("confirm_password")!=request.form.get("password"):
            return "<h1> Passwords do not match ): </h1>"
        


        data = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        if data:
            return "<h1> Username Already Taken </h1>"
        
        
        db.execute("INSERT INTO users (username,hash) VALUES(?, ?)",request.form.get("username"),request.form.get("password"))
        rows = db.execute("SELECT * FROM users WHERE username = ?",request.form.get("username"))
        session["user_id"] = rows[0]["id"]

        return redirect("/")

    
@app.route("/logout")
def logout():
    session.clear()
    return redirect('/login')