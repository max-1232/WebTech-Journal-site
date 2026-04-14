from flask import Blueprint, render_template, redirect, url_for, request, flash
from journal_app.models import Entry, db

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
        return redirect(url_for('home'))
    
    return render_template('create_entry.html', title='Nieuw Bericht')
