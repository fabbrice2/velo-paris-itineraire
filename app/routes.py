from app import app
from flask import Flask, redirect, render_template, session, url_for, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from config import db
import requests


cursor = db.cursor()


@app.route("/", methods=["POST", "GET"])
def home():
    # if "username" in session:
    #     username = session["username"]
    #     return render_template("home.html.jinja", username=username)
    # else:
    return render_template("home.html.jinja")

def get_data_from_url():
    url = "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/velib-disponibilite-en-temps-reel/records?limit=20"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(data['results'])
        return data['results']
    else:
        return None


# Route to retrieve the Velib data
@app.route('/velib', methods=['GET'])
def get_velib_data():
    data = get_data_from_url()
    if data:
        # return jsonify(data)
        return render_template('listes_velib.html.jinja', records=data)
    else:
        return jsonify({"error": "Failed to fetch Velib data"})


@app.route("/login/", methods=["POST", "GET"])
def login():
    errormsg = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        cursor.execute("SELECT * FROM accounts where username = %s", (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user[2], password):
            session["id"] = user[0]
            session["username"] = user[1]
            session["email"] = user[3]
            session["password"] = user[2]
            return redirect(url_for("home"))
        else:
            errormsg = "Email ou mot de passe incorrect"

    return render_template("login.html.jinja", errormsg=errormsg)


@app.route("/register/", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])

        cursor.execute(
            "INSERT INTO accounts (username, email, password) VALUES (%s, %s, %s)",
            (username, email, password),
        )
        db.commit()

        return redirect(url_for("login"))

    return render_template("register.html.jinja")


@app.route("/logout/")
def logout():
    session.pop("username")
    session.pop("email")
    session.pop("password")
    session.pop("id")
    return redirect(url_for("login"))


@app.route("/profil/")
def profil():
    if "username" in session:
        username = session["username"]
        email = session["email"]
        password = session["password"]
    return render_template(
        "profil.html.jinja", username=username, email=email, password=password
    )


@app.route("/updateProfil/", methods=["POST", "GET"])
def updateProfil():
    if "id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]

        cursor.execute(
            "UPDATE accounts SET username = %s, email = %s WHERE id = %s",
            (username, email, session["id"]),
        )
        db.commit()
        session["username"] = username
        session["email"] = email

        return redirect(url_for("home"))

    return render_template("updateProfil.html.jinja")
