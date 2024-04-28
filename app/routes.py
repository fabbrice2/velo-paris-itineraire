# Importation des modules Flask et des dépendances nécessaires
from app import app
from flask import Flask, redirect, render_template, session, url_for, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from config import db
import requests
import time

# Initialisation du curseur pour la base de données
cursor = db.cursor()

# Route principale de l'application
@app.route("/", methods=["GET"])
def home():
    # Récupération des données depuis une URL externe
    data = get_data_from_url()
    if data:
        # Extraction des coordonnées des stations
        coordinates = extract_coordinates(data)
        # Insertion des données des stations dans la base de données
        insert_station_data(data)
        # Rendu de la page d'accueil avec les données et les coordonnées des stations
        return render_template("home.html.jinja", records=data, coordinates=coordinates)
    if "username" in session:
        # Si l'utilisateur est connecté, afficher la page d'accueil avec son nom d'utilisateur
        username = session["username"]
        return render_template("home.html.jinja", username=username)
    # Sinon, afficher simplement la page d'accueil
    return render_template("home.html.jinja")

# Fonction pour insérer les données des stations dans la base de données
def insert_station_data(data):
    for record in data:
        try:
            # Extraction des informations sur la station
            station_id = record["stationcode"]
            location = record["name"]
            bike_number_available = record["numbikesavailable"]
            mechanical_bike_count = record["mechanical"]
            electric_bike_count = record["ebike"]
            available_parking_spots = record["numdocksavailable"]
            # Insertion des données dans la base de données
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
            # Affichage d'un message de succès si l'insertion est réussie
            print(
                f"les donnees de la station {station_id} ont ete inserees avec succes."
            )
        except KeyError as e:
            # Gestion des erreurs liées aux clés manquantes dans les données
            print(f"erreur lors de linsertion des donnees: {e}")
            pass
        except Exception as e:
            # Gestion des autres erreurs lors de l'insertion des données
            print(f"une erreur sest produite lors de linsertion des donnees: {e}")
            pass

# Fonction pour récupérer les données depuis une URL externe
def get_data_from_url():
    url = "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/velib-disponibilite-en-temps-reel/records?limit=20"
    response = requests.get(url)
    if response.status_code == 200:
        # Si la requête réussit, retourner les données au format JSON
        data = response.json()
        print(data["results"])
        return data["results"]
    else:
        # Sinon, retourner None
        return None

# Fonction pour extraire les coordonnées des stations depuis les données
def extract_coordinates(data):
    coordinates = []
    for record in data:
        try:
            # Extraction des coordonnées et d'autres informations sur la station
            lon = record["coordonnees_geo"]["lon"]
            lat = record["coordonnees_geo"]["lat"]
            mechanical = (record["mechanical"],)
            name = record["name"]
            ebike = record["ebike"]
            numdocksavailable = record["numdocksavailable"]
            location = record["name"]
            stationcode = record["stationcode"]
            # Ajout des informations dans la liste des coordonnées
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
            # Ignorer les stations sans coordonnées
            pass
    return coordinates

# Route pour la connexion des utilisateurs
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
                # Initialisation de la session si l'utilisateur est authentifié
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

# Route pour l'inscription des nouveaux utilisateurs
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
            # Insertion des nouvelles informations dans la base de données
            cursor.execute(
                "INSERT INTO accounts (username, password, email) VALUES (%s, %s, %s)",
                (username, password, email),
            )
            db.commit()
            return redirect(url_for("login"))

    return render_template("register.html.jinja", errormsg=errormsg)

# Route pour la déconnexion des utilisateurs
@app.route("/logout/")
def logout():
    # Suppression des informations de session lors de la déconnexion
    session.pop("username")
    session.pop("email")
    session.pop("password")
    session.pop("id")
    return redirect(url_for("login"))

# Route pour afficher le profil de l'utilisateur
@app.route("/profil/")
def profil():
    if "username" in session:
        username = session["username"]
        email = session["email"]
  
    return render_template(
        "updateProfil.html.jinja",username=username, email=email,
    )

# Route pour mettre à jour le profil de l'utilisateur
@app.route("/updateProfil/", methods=["POST", "GET"])
def updateProfil():
    if "id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]

        # Mise à jour des informations dans la base de données
        cursor.execute(
            "UPDATE accounts SET username = %s, email = %s WHERE id = %s",
            (username, email, session["id"]),
        )
        db.commit()
        session["username"] = username
        session["email"] = email
       
        return redirect(url_for("home"))

    return render_template("updateProfil.html.jinja")

# Route pour ajouter des favoris
@app.route('/favorites', methods=['POST'])
def add_favorite(): 
    if 'id' in session:

        user_id = session['id']
        
        station_name = request.form.get('station_name')
        station_id = request.form.get('station_id')
        nomFavoris = request.form.get('nomFavoris')
        
        try:
  
            # Insertion des favoris dans la base de données
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

# Route pour afficher les favoris
@app.route("/favoritesall")
def show_favorites(): 
    if "id" in session:
        user_id = session["id"]
        try:
            # Sélection des favoris de l'utilisateur depuis la base de données
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

# Route pour définir l'emplacement d'un favori
@app.route("/define_location", methods=["POST"])
def define_location():
    favorite_id = request.form["favorite_id"]
    location = request.form["location"]
    try:
        # Mise à jour de l'emplacement du favori dans la base de données
        cursor.execute(
            "UPDATE favorite_relations SET user_location_name = %s WHERE id_favorite = %s",
            (location, favorite_id),
        )
        db.commit()
        return redirect(request.referrer)
    except Exception as e:
        return f"Error: {e}", 500

# Route pour supprimer un favori
@app.route("/delete_favorite", methods=["POST"])
def delete_favorite():
    favorite_id = request.form["favorite_id"]

    try:
        # Suppression du favori de la base de données
        cursor.execute(
            "DELETE FROM favorite_relations WHERE id_favorite = %s", (favorite_id,)
        )
        db.commit()
        return redirect(url_for("show_favorites"))
    except Exception as e:
        return f"Error: {e}", 500

# Route pour ajouter un nom de favori
@app.route('/addname', methods=["POST"])
def addname():
    if 'id' in session:

        user_id = session['id']
        station_name = request.form.get('station_name')
        station_id = request.form.get('station_id') 
          
        return render_template("ajouterFavoris.html.jinja",station_name=station_name,station_id=station_id,user_id = user_id)
    else :
        return redirect(url_for("login"))

# Route pour afficher la liste des favoris
@app.route("/updatefav")
def updatefav():
    if "id" not in session:
        return redirect(url_for("login"))
    print("erreur")
    return render_template("favoris-list.html.jinja")
