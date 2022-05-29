from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
    return render_template("home.html", user=current_user)

@views.route('/update/<int:id>', methods=['POST', 'GET'])
def update_note(id):
    note_to_update = Note.query.get_or_404(id)
    if request.method == "POST":
        note_to_update.note = request.form['noteId']
        try:
            db.session.commit()
            return render_template("home.html", user=current_user)
        except:
            return "Uh oh, there was a problem."
    else:
        return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data.decode('utf-8'))
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            flash('Note deleted!', category="success")
    #return render_template("home.html", user=current_user)
    return jsonify({})