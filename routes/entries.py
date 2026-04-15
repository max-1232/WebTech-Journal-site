from flask import Blueprint, render_template, redirect, url_for, request, flash
from models import Entry, db
from flask_login import current_user, login_required
# aanmaken van de blueprint voor de app.py file
entries_bp = Blueprint('entries', __name__)

# Route aanmaken voor nieuwe entries 
@entries_bp.route('/entry/new', methods=["GET", "POST"])
def new_entry():
    """Functie waarmee nieuwe entries gemaakt kunnen worden die worden opgeslagen in de database"""
    if request.method == 'POST': # ontvangt de ingevulde titel en content van de entry
        title = request.form.get('title')
        content = request.form.get('content')

    # Geeft een melding dat de titel verplicht is als deze niet is ingevuld maar wel een content
        if not title or not content:
            flash("Titel en inhoud zijn verplicht!", "danger")
            return redirect(url_for('entries.new_entry'))

    # Maak de nieuwe entry aan en koppel deze aan de huidige gebruiker via current_user.id
        entry = Entry(title=title, content=content, user_id=current_user.id) #type: ignore
        db.session.add(entry)
        db.session.commit() # Voegt de gegevens toe aan de database en slaat deze op
        flash("Je bericht is geplaatst!", "success")
        return redirect(url_for('main.home'))
    return render_template('create_entry.html', title='Nieuw Bericht')

# Route aanmaken om entries te bewerken 
@entries_bp.route("/entry/<int:entry_id>/update", methods=['GET', 'POST'])
@login_required
def update_entry(entry_id):
    """Functie om een entry te bewerken en om deze opnieuw op te slaan"""
    entry = Entry.query.get_or_404(entry_id)

    # Geeft een error als de user_id niet gelijk is aan de opgeslagen id die past bij de entry
    if entry.author != current_user:
        return "Dit is niet jouw bericht!", 403
    if request.method == 'POST':
        entry.title = request.form.get('title')
        entry.content = request.form.get('content')
        db.session.commit()
        flash("Je bericht is succesvol bewerkt!", "success")
        return redirect(url_for('main.home'))
    return render_template('create_entry.html', title='Update Entry', entry=entry)

# Route aanmaken om entries te verwijderen
@entries_bp.route("/entry/<int:entry_id>/delete", methods=['POST'])
@login_required
def delete_entry(entry_id):
    """Functie die entries verwijdert en uit de database haalt.
    Kijkt of de entry bij de ingelogde user hoort."""
    entry = Entry.query.get_or_404(entry_id)
    if entry.author != current_user:
        return "Niet toegestaan", 403
    
    db.session.delete(entry)
    db.session.commit()
    flash("Je bericht is succesvol verwijderd!", )
    return redirect(url_for('main.home'))