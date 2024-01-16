from flask import Flask , render_template , redirect , request , session
from werkzeug.security import generate_password_hash,check_password_hash
from flask_session import Session




app = Flask(__name__)


app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def index():
    return render_template("index.html")