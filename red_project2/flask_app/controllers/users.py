from flask import render_template, request, redirect, session, flash
from flask_app import app, bcrypt
from flask_app.models.user import User

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/register/user", methods=['POST'])
def register():
    print(request.form)
    if not User.validate_user(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password" : pw_hash
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    session['first_name'] = request.form['first_name']
    return redirect('/paintings')

@app.route('/login', methods=['post'])
def login():
    data = {'email': request.form['email']}
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash('invalid credentials')
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        return redirect('/')
    session['user_id'] = user_in_db.id
    session['first_name'] = user_in_db.first_name
    return redirect('/paintings')

    # ! edit user
@app.route('/users/edit/<int:id>')
def edit(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {'id': id}
    
    return render_template('edit.html', user=User.get_one_with_painting(data))

@app.route('/edit/user', methods=['POST'])
def wrangle_edit():
    if not User.update_user(request.form):
        return redirect(f"/users/edit/{session['user_id']}")
    print(request.form)
    data = {
        'id': session['user_id'],
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        'email': request.form['email']
    }
    
    User.update(data)
    return redirect('/paintings')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')