from flask import Flask, render_template, url_for, flash, redirect, request, make_response
from models import db, User, Entry
import os
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'jouw_geheime_code'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager: LoginManager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # type: ignore

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Route naar de home pagina
@app.route("/")
def home():
    if current_user.is_authenticated:
        # Haal alleen de entries van de ingelogde gebruiker op, nieuwste bovenaan
        entries = Entry.query.filter_by(user_id=current_user.id).order_by(Entry.date_posted.desc()).all()
    else:
        entries = []
    
    return render_template('index.html', entries=entries)

# Route naar de register pagina
@app.route("/register", methods=['GET', 'POST'])
def register() -> str:
    """Register pagina"""
    if request.method == 'POST':
        print("Formulier ontvangen!")
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        if not username or not email or not password:
            return make_response("Vul alles in", 400) # type: ignore

        print(f"Data: {username}, {email}")
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "Deze gebruikersnaam bestaat al!"

        
        # Maak nieuwe gebruiker aan
        hashed_pw = generate_password_hash(password, method='pbkdf2:sha256')
        print(f"Hashed password: {hashed_pw}")
        new_user = User(username=username, email=email, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        print("Gebruiker opgeslagen?")

        # Na registratie sturen we ze naar de homepagina
        redirect(url_for('home'))
    return render_template('register.html')

# Route naar de login page
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if password and user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            return "Inloggen mislukt. Check je gegevens."

    return render_template('login.html')

# Route om uit te loggen, je moet ingelogd is hier required
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/entry/new", methods=['GET', 'POST'])
@login_required
def new_entry():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        # Validatie: Check of velden niet None of leeg zijn (voorkomt Pylance errors)
        if not title or not content:
            flash("Titel en inhoud zijn verplicht!", "danger")
            return redirect(url_for('new_entry'))

        # Maak de nieuwe entry aan en koppel deze aan de huidige gebruiker via current_user.id
        entry = Entry(title=title, content=content, user_id=current_user.id) #type: ignore
        
        db.session.add(entry)
        db.session.commit()
        
        flash("Je bericht is geplaatst!", "success")
        return redirect(url_for('home'))
        
    return render_template('create_entry.html', title='Nieuw Bericht')


@app.route("/entry/<int:entry_id>/update", methods=['GET', 'POST'])
@login_required
def update_entry(entry_id):
    entry = Entry.query.get_or_404(entry_id)
    if entry.author != current_user:
        return "Dit is niet jouw bericht!", 403
    if request.method == 'POST':
        entry.title = request.form.get('title')
        entry.content = request.form.get('content')
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('create_entry.html', title='Update Entry', entry=entry)

@app.route("/entry/<int:entry_id>/delete", methods=['POST'])
@login_required
def delete_entry(entry_id):
    entry = Entry.query.get_or_404(entry_id)
    if entry.author != current_user:
        return "Niet toegestaan", 403
    
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for('home'))

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