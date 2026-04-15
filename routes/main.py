from flask import Flask, render_template, Blueprint
from flask_login import current_user
from models import db, Entry, User

# Een blueprint maken voor de app.py file
main_bp = Blueprint('main', __name__)

# Aanmaken van de route voor de home pagina 
@main_bp.route("/")
def home():
    """Functie die de home pagina aanmaakt"""
    if current_user.is_authenticated:
        # Haal alleen de entries van de ingelogde gebruiker op, nieuwste bovenaan
        entries = Entry.query.filter_by(user_id=current_user.id).order_by(Entry.date_posted.desc()).all()
    else:
        entries = []
    
    return render_template('index.html', entries=entries)