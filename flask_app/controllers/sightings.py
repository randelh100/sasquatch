from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.sighting import Sighting
from flask_app.models.user import User


@app.route('/sightings')
def dashboard():
    if 'user_id' not in session:
        flash('You must be logged in to view')
        return redirect('/')
    return render_template('sightings.html', user=User.get_one({'id' : session['user_id']}), sightings=Sighting.get_all())


@app.route('/new/sighting/create', methods=['POST'])
def new_sighting():
    if 'user_id' not in session:
        flash('You must be logged in to create a new sighting')
        return redirect('/')
    data = {
        'location' : request.form['location'],
        'date' : request.form['date'],
        'what_happened' : request.form['what_happened'],
        'amount' : request.form['amount'],
        'user_id' : session['user_id']
    }
    if not Sighting.validate_sighting(request.form):
        return redirect('/report/sighting')
    Sighting.save(data)
    return redirect('/sightings')

@app.route('/edit/<int:id>')
def edit_sighting(id):
    if 'user_id' not in session:
        flash('You must be logged in to edit a sighting')
        return redirect('/')
    
    sighting = Sighting.get_one({'id': id})
    return render_template('edit_sighting.html', sighting=sighting, user=User.get_one({'id': session['user_id']}))

@app.route('/edit/sighting/<int:id>', methods=['POST'])
def update_sighting(id):
    if 'user_id' not in session:
        flash('You must be logged in to edit a sighting')
        return redirect('/')
    data = {
        'location' : request.form['location'],
        'date' : request.form['date'],
        'what_happened' : request.form['what_happened'],
        'amount' : request.form['amount'],
        'id' : id
    }
    if not Sighting.validate_sighting(request.form):
        return redirect(f'/edit/{id}')
    Sighting.update(data)
    return redirect('/sightings')


@app.route('/delete/<int:id>')
def delete_sighting(id):
    if 'user_id' not in session:
        flash('You must be logged in to delete a sighting')
        return redirect('/')
    data={'id':id}
    Sighting.delete(data)
    return redirect('/sightings')


@app.route('/report/sighting')
def create_sighting():
    if 'user_id' not in session:
        flash('You must be logged in to create a new sighting')
        return redirect('/')
    
    return render_template('new_sighting.html', user=User.get_one({'id': session['user_id']}))


@app.route('/view/<int:id>')
def view_sighting(id):
    if 'user_id' not in session:
        flash('You must be logged in to view a sighting')
        return redirect('/')
    data = {
        'id': id,
    }
    sighting = Sighting.get_one(data)
    return render_template('view_sighting.html', sighting=sighting, user=User.get_one({'id': session['user_id']}), skeptics=Sighting.get_users_that_are_skeptic(data), is_skeptic=Sighting.is_user_skeptic({'sighting_id': id, 'user_id': session['user_id']}))

@app.route('/skeptic/<int:id>')
def skeptic(id):
    if 'user_id' not in session:
        flash('You must be logged in to view')
        return redirect('/')
    data = {
        'sighting_id': id,
        'user_id': session['user_id']
    }
    Sighting.create_skeptic(data)
    return redirect(f'/view/{id}')


@app.route('/skeptic/remove/<int:id>')
def remove_skeptic(id):
    if 'user_id' not in session:
        flash('You must be logged in to view')
        return redirect('/')
    data = {
        'sighting_id': id,
        'user_id': session['user_id']
    }
    Sighting.delete_skeptic(data)
    return redirect(f'/view/{id}')