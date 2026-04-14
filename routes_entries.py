from flask import Blueprint, render_template, redirect, url_for, request, flash
from models import Entry, db
from flask_login import current_user, login_required

entries_bp = Blueprint('entries', __name__)

@entries_bp.route('/entry/new', methods=["GET", "POST"])
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
        return redirect(url_for('main.home'))
    return render_template('create_entry.html', title='Nieuw Bericht')

@entries_bp.route("/entry/<int:entry_id>/update", methods=['GET', 'POST'])
@login_required
def update_entry(entry_id):
    entry = Entry.query.get_or_404(entry_id)
    if entry.author != current_user:
        return "Dit is niet jouw bericht!", 403
    if request.method == 'POST':
        entry.title = request.form.get('title')
        entry.content = request.form.get('content')
        db.session.commit()
        flash("Je bericht is succesvol bewerkt!", "success")
        return redirect(url_for('main.home'))
    return render_template('create_entry.html', title='Update Entry', entry=entry)

@entries_bp.route("/entry/<int:entry_id>/delete", methods=['POST'])
@login_required
def delete_entry(entry_id):
    entry = Entry.query.get_or_404(entry_id)
    if entry.author != current_user:
        return "Niet toegestaan", 403
    
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for('main.home'))