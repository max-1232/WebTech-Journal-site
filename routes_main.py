from flask import Flask, render_template, Blueprint
from flask_login import current_user
from models import db, Entry, User

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
def home():
    if current_user.is_authenticated:
        # Haal alleen de entries van de ingelogde gebruiker op, nieuwste bovenaan
        entries = Entry.query.filter_by(user_id=current_user.id).order_by(Entry.date_posted.desc()).all()
    else:
        entries = []
    
    return render_template('index.html', entries=entries)