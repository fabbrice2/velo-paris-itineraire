from app import app
from flask import Flask, redirect, render_template, session, url_for, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from config import db
import requests
import time

cursor = db.cursor()


@app.route("/", methods=["GET"])
def home():
    data = get_data_from_url()
    if data:
        coordinates = extract_coordinates(data)
        insert_station_data(data)
        return render_template("home.html.jinja", records=data, coordinates=coordinates)
    if "username" in session:
        username = session["username"]
        return render_template("home.html.jinja", username=username)
    return render_template("home.html.jinja")


def insert_station_data(data):
    for record in data:
        try:
            station_id = record["stationcode"]
            location = record["name"]
            bike_number_available = record["numbikesavailable"]
            mechanical_bike_count = record["mechanical"]
            electric_bike_count = record["ebike"]
            available_parking_spots = record["numdocksavailable"]
            cursor.execute(
                "INSERT INTO station (id_station, location, bike_number_available, mechanical_bike_count, electric_bike_count, available_parking_spots) VALUES (%s, %s, %s, %s, %s, %s)",
                (
                    station_id,
                    location,
                    bike_number_available,
                    mechanical_bike_count,
                    electric_bike_count,
                    available_parking_spots,
                ),
            )
            db.commit()
            print(
                f"les donnees de la station {station_id} ont ete inserees avec succes."
            )
        except KeyError as e:
            print(f"erreur lors de linsertion des donnees: {e}")
            pass
        except Exception as e:
            print(f"une erreur sest produite lors de linsertion des donnees: {e}")
            pass


def get_data_from_url():
    url = "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/velib-disponibilite-en-temps-reel/records?limit=20"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(data["results"])
        return data["results"]
    else:
        return None


def extract_coordinates(data):

    coordinates = []
    for record in data:
        try:
            lon = record["coordonnees_geo"]["lon"]
            lat = record["coordonnees_geo"]["lat"]
            mechanical = (record["mechanical"],)
            name = record["name"]
            ebike = record["ebike"]
            numdocksavailable = record["numdocksavailable"]
            location = record["name"]
            stationcode = record["stationcode"]

            coordinates.append(
                {
                    "lon": lon,
                    "lat": lat,
                    "mechanical": mechanical,
                    "name": name,
                    "ebike": ebike,
                    "numdocksavailable": numdocksavailable,
                    "location": location,
                    "stationcode": stationcode,
                }
            )
        except KeyError:
            pass
    return coordinates


@app.route("/login/", methods=["POST", "GET"])
def login():
    errormsg = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        cursor.execute("SELECT * FROM accounts WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user:
            if check_password_hash(user[2], password):
                session["id"] = user[0]
                session["username"] = user[1]
                session["email"] = user[3]
                session["password"] = user[2]
                return redirect(url_for("home"))
            else:
                errormsg = "Mot de passe incorrect"
        else:
            errormsg = "Nom d'utilisateur incorrect"

    return render_template("login.html.jinja", errormsg=errormsg)


@app.route("/register/", methods=["POST", "GET"])
def register():
    errormsg = ""
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])
        email = request.form["email"]

        cursor.execute("SELECT * FROM accounts WHERE email = %s", (email,))
        existing_email = cursor.fetchone()

        cursor.execute("SELECT * FROM accounts WHERE username = %s", (username,))
        existing_username = cursor.fetchone()

        if existing_email:
            errormsg = "Email déjà existant"
        elif existing_username:
            errormsg = "Nom d'utilisateur déjà existant."
        else:
            cursor.execute(
                "INSERT INTO accounts (username, password, email) VALUES (%s, %s, %s)",
                (username, password, email),
            )
            db.commit()
            return redirect(url_for("login"))

    return render_template("register.html.jinja", errormsg=errormsg)


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
  
    return render_template(
        "updateProfil.html.jinja",username=username, email=email,
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


@app.route('/favorites', methods=['POST'])
def add_favorite(): 
    if 'id' in session:

        user_id = session['id']
        
        station_name = request.form.get('station_name')
        station_id = request.form.get('station_id')
        nomFavoris = request.form.get('nomFavoris')
        
        try:
  
            cursor.execute(
                "INSERT INTO favorite_relations (favorite_name, user_id, station_id ,user_location_name) VALUES (%s, %s, %s,%s)",
                (station_name, user_id, station_id ,nomFavoris)
            )
            db.commit()
            print("donnee insere avec succes .")
            
            return redirect(url_for('show_favorites'))
            
        except Exception as e:
            print(f"erreur lors de l'insertion : {e}")
            return jsonify({"error": "erreur lors de l'insertion."}), 500
    else:
        return redirect(url_for('login'))



@app.route("/favoritesall")
def show_favorites(): 
    if "id" in session:
        user_id = session["id"]
        try:
            cursor.execute(
                "SELECT * FROM favorite_relations WHERE user_id = %s", (user_id,)
            )
            favorites = cursor.fetchall()

            return render_template("favorites.html.jinja", favorites=favorites)
        except Exception as e:
            return (
                jsonify({"error": "Erreur lors de la récupération des favoris."}),
                500,
                print(e)
            )
    else:
        return redirect(url_for("login"))


@app.route("/define_location", methods=["POST"])
def define_location():
    favorite_id = request.form["favorite_id"]
    location = request.form["location"]
    try:
        cursor.execute(
            "UPDATE favorite_relations SET user_location_name = %s WHERE id_favorite = %s",
            (location, favorite_id),
        )
        db.commit()
        return redirect(request.referrer)
    except Exception as e:
        return f"Error: {e}", 500


@app.route("/delete_favorite", methods=["POST"])
def delete_favorite():
    favorite_id = request.form["favorite_id"]

    try:
        cursor.execute(
            "DELETE FROM favorite_relations WHERE id_favorite = %s", (favorite_id,)
        )
        db.commit()
        return redirect(url_for("show_favorites"))
    except Exception as e:
        return f"Error: {e}", 500
    





@app.route('/addname', methods=["POST"])
def addname():
    if 'id' in session:

        user_id = session['id']
        station_name = request.form.get('station_name')
        station_id = request.form.get('station_id') 
          
        return render_template("ajouterFavoris.html.jinja",station_name=station_name,station_id=station_id,user_id = user_id)
    else :
        return redirect(url_for("login"))
    


    
# @app.route('/addFavorite', methods=['POST'])
# def addFavorite():
    
#     if "id" in session:
#         user_id = session["id"]
#         try:
#             cursor.execute(
#                 "SELECT * FROM favorite_relations WHERE user_id = %s", (user_id,)
#             )
#             favorites = cursor.fetchone()

#             return render_template("favorites.html.jinja", favorites=favorites)
#         except Exception as e:
#             return (
#                 jsonify({"error": "Erreur lors de la récupération des favoris."}),
#                 500,
#             )
#     else:
#         return redirect(url_for("login"))

    
    # return render_template('addFavorite.html.jinja')





    # ....................siaka.....................

# 
# @app.route("/favoritessiaka")
# def favorissiaka():
#     if "id" not in session:
#         return redirect(url_for("login"))
#     if "username" in session:
#         username = session["username"]
#     return render_template("mesFavoris.html.jinja", username=username)

# @app.route('/ajouterFavorissiaka')
# def ajouterFavorissiaka():
#     if "id" not in session:
#         return redirect(url_for("login"))
#     return render_template("ajouterFavoris.html.jinja")


# @app.route("/afficheFavori")
# def afficheFavori():
#     if "id" in session:
#         user_id = session["id"]
#         try:
#             cursor.execute(
#                 "SELECT * FROM favorite_relations WHERE user_id = %s", (user_id,)
#             )
#             favorites = cursor.fetchall()

#             return render_template("mesFavoris.html.jinja", favorites=favorites)
#         except Exception as e:
#             return (
#                 jsonify({"error": "Erreur lors de la récupération des favoris."}),
#                 500,
#                 print(e)
#             )
#     else:
#         return redirect(url_for("login"))


@app.route("/updatefav")
def updatefav():
    if "id" not in session:
        return redirect(url_for("login"))
    print("erreur")
    return render_template("favoris-list.html.jinja")

