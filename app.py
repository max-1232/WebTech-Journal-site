from flask import Flask, render_template, url_for, flash, redirect
from models import db, User, Entry
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'jouw_geheime_code'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route("/")
def base() -> str:
    """Homepage"""
    all_users = User.query.all()
    return render_template("index.html", users=all_users)

# @app.route("/home")
# def home() -> str:
#     entries = Entry.query.all()
#     """Homepage route"""
#     return render_template('index.html', entries=entries)

@app.route("/entry/<int:entry_id>")
def entry(entry_id):
    entry = Entry.query.get_or_404(entry_id)
    return render_template('entry.html', title=entry.title, entry=entry)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        if User.query.count() == 0:
            print("Database is leeg, test-gebruikers toevoegen...")
            user1 = User(username="Max", email="max@gmail.com", password="hallo123") 
            user2 = User(username="Pieter", email="pieter@gmail.com", password="123hallo") 
            db.session.add_all([user1, user2])
            db.session.commit()
            print("Gebruikers succesvol toegevoegd!")
        else:
            print("Gebruikers bestonden al.")

    app.run(debug=True)