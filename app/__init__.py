from flask import Flask
from flask import session
import os

app = Flask(__name__)

app.secret_key = os.urandom(24)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'pythonlogin'


from app import routes
