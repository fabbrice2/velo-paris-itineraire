from flask import Flask
import os

app = Flask(__name__)

# Génération d'une clé secrète aléatoire
app.secret_key = os.urandom(24)

from app import routes
