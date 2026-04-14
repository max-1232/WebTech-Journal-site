from flask import Blueprint, render_template, redirect, url_for, flash, request
from models import db, User, Entry
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, login_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register() -> str:
    """Register pagina waar de gebruiker een account kan aanmaken"""
    # Als het formulier is afgestuurd en ontvangen is met de gegevens
    if request.method == 'POST':
        print("Formulier ontvangen!")
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        # als niet alles is ingevuld geef dat aan 
        if not username or not email or not password:
            return make_response("Vul alles in", 400) # type: ignore

        print(f"Data: {username}, {email}")
        # Controleert in de database of de gebruiker al bestaat
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "Deze gebruikersnaam bestaat al!"

        # Hashed het wachtwoord die vervolgens wordt opgeslagen in de tabel Entry
        hashed_pw = generate_password_hash(password, method='pbkdf2:sha256')
        print(f"Hashed password: {hashed_pw}")
        new_user = User(username=username, email=email, password=hashed_pw)
        db.session.add(new_user) 
        db.session.commit() # Slaat de nieuwe gebruiker op en print dit
        print("Gebruiker opgeslagen?")

        # Na de registratie wordt de user terug gestuurd naar de home pagine
        redirect(url_for('main.home'))
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login pagina waar een gebruiker kan inloggen op een betaand account"""
    # ontvangt hier de gegevens die zijn ingevuld in het login formulier
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        # kijkt of het wachtwoord hash klopt met wat in de databse staat en logt de user vervolgens in 
        if password and user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('main.home'))
        else: # Anders komt deze error
            return "Inloggen mislukt. Check je gegevens."
    return render_template('login.html')

@auth_bp.route("/logout")
@login_required
def logout():
    """Simpele logout functie die je laat uitloggen met een knop in de menubalk"""
    logout_user()
    flash('Je bent nu uitgelogd!', "success")
    return redirect(url_for('main.home'))