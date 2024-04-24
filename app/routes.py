from app import app
from flask import Flask, redirect, render_template, session, url_for, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from config import db
import requests
import time
import requests
from flask import session


cursor = db.cursor()

def insert_station_data(data):
    for record in data:
        try:
            station_id = record['stationcode'] 
            location = record['name']
            bike_number_available = record['numbikesavailable']
            mechanical_bike_count = record['mechanical']
            electric_bike_count = record['ebike']
            available_parking_spots = record['numdocksavailable']
            cursor.execute(
                "INSERT INTO station (id_station, location, bike_number_available, mechanical_bike_count, electric_bike_count, available_parking_spots) VALUES (%s, %s, %s, %s, %s, %s)",
                (station_id, location, bike_number_available, mechanical_bike_count, electric_bike_count, available_parking_spots)
            )
            db.commit()
            print(f"les donnees de la station {station_id} ont ete inserees avec succes.")
        except KeyError as e:
            print(f"erreur lors de linsertion des donnees: {e}")
            pass
        except Exception as e:
            print(f"une erreur sest produite lors de linsertion des donnees: {e}")
            pass




@app.route("/", methods=["POST", "GET"])
def home():
    # if "username" in session:
    #     username = session["username"]
    #     return render_template("home.html.jinja", username=username)
    # else:
    return render_template("home.html.jinja")

def get_data_from_url():
    # Modification de Aboubakar
    global cached_data, Last_Update_Time

    # Modification de Aboubakar
    cached_data = None
    Last_Update_Time = None


    # Modification de Aboubakar
    if cached_data is not None and Last_Update_Time is not None:
        if time.time() - Last_Update_Time > 300:
            print("Les données en cache sont périmées. Récupération de nouvelles données...")
            return cached_data 

    url = "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/velib-disponibilite-en-temps-reel/records?limit=20"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        # Modification de Aboubakar
        cached_data = data['results']
        Last_Update_Time = time.time()
        print("Nouvelles données récupérées et mises en cache.")
        return data['results']
    else:
        print("La récupération des données a échoué.")
        return None


def extract_coordinates(data):
    
    coordinates = []
    for record in data:
        try:
            lon = record['coordonnees_geo']['lon']
            lat = record['coordonnees_geo']["lat"]
            coordinates.append({"lon": lon, "lat": lat})
        except KeyError:
            pass  
    return coordinates

@app.route('/velib', methods=['GET'])
def get_velib_data():
    data = get_data_from_url()
    if data:
        coordinates = extract_coordinates(data)
        insert_station_data(data) 
        return render_template('listes_velib.html.jinja', records=data, coordinates=coordinates)
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
            
            # Afficher l'ID de l'utilisateur
            print(f"ID de l'utilisateur : {user[0]}")
            
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

from flask import session

from flask import session

from flask import request

@app.route('/favorites', methods=['POST'])
def add_favorite():
    if 'id' in session:
        user_id = session['id']
        
        station_name = request.form.get('station_name')
        station_id = request.form.get('station_id')

        
        try:
  
            cursor.execute(
                "INSERT INTO favorite_relations (favorite_name, user_id, station_id) VALUES (%s, %s, %s)",
                (station_name, user_id, station_id)
            )
            db.commit()
            print("Données de favoris insérées avec succès.")
            return redirect(request.referrer)
        except Exception as e:
            print(f"Erreur lors de l'insertion des données de favoris : {e}")
            return jsonify({"error": "Erreur lors de l'insertion des données de favoris."}), 500
    else:
        return redirect(url_for('login'))



