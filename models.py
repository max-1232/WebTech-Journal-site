from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, timezone

db = SQLAlchemy()
# User tabel voor de database
class User(db.Model, UserMixin):
    """Id met primary key, een username, een email en een wachtwoord"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    entries = db.relationship('Entry', backref='author', lazy=True)

    # Voor de registratie om de gegevens juist in te vullen
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

# Entry tabel waar alle verhalen/entries worden opgeslagen samen met de titel, datum en de user_id van de schrijver
class Entry(db.Model):
    """Tabel voor de entries met een id, de titel, wanneer hij is geplaatst, de content van de entry en de user_id die gelinkt is met de user tabel"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

