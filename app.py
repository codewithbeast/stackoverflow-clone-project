from flask import Flask , render_template , redirect , request , session
from werkzeug.security import generate_password_hash,check_password_hash
from flask_session import Session

from functions import *


app = Flask(__name__)


app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

connection = sqlite3.connect("users.db")
query = connection.cursor()

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
        

        db,query = get_db()

        username = request.form.get("username")
        data = query.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchall()

        if len(data) !=1 or not check_password_hash(data[0][2],request.form.get("password")):
            return "<h1 Invalid Username/Password </h1>"
        

        session["user_id"] = data[0][0]

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
        
        db,query = get_db()

        data = query.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),)).fetchall()

        if data:
            return "<h1> Username Already Taken </h1>"
        
        values = [
            (request.form.get("username"),(generate_password_hash(request.form.get("password"))))
            
        ]
        query.executemany("INSERT INTO users (username,hash) VALUES(?, ?)", values)
        db.commit()
        rows = query.execute("SELECT * FROM users WHERE username = ?",(request.form.get("username"),)).fetchall()
        session["user_id"] = rows[0][0]

        return redirect("/")

    
@app.route("/logout")
def logout():
    session.clear()
    return redirect('/login')