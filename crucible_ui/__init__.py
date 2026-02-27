from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize Flask app
app = Flask(__name__)

# Configure database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'crucible-turbine-secret-key-2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, '..', 'instance', 'crucible.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Google OAuth Configuration
app.config['GOOGLE_CLIENT_ID'] = os.environ.get('GOOGLE_CLIENT_ID')
app.config['GOOGLE_CLIENT_SECRET'] = os.environ.get('GOOGLE_CLIENT_SECRET')

# Initialize database
db = SQLAlchemy(app)

from crucible_ui import routes