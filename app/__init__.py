from flask import Flask, render_template

app = Flask(__name__)

# Importez vos routes depuis routes.py
from app import routes
