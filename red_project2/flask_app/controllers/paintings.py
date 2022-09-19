from flask import render_template, request, redirect, session
from flask_app import app
from flask_app.models.painting import Painting

# ! ////// CREATE  //////
# TODO CREATE REQUIRES TWO ROUTES:
# TODO ONE TO DISPLAY THE FORM:
@app.route('/painting/new')
def new_painting():
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template("new_painting.html")

# TODO ONE TO HANDLE THE DATA FROM THE FORM
@app.route('/painting/create',methods=['POST'])
def create_painting():
    if not Painting.add_painting(request.form):
        return redirect('/painting/new')
    print(request.form)
    # painting_data = {
    #     'id': session['user_id'],
    #     "title": request.form['title'],
    #     "description": request.form['description'],
    #     'price': request.form['price']
    # }
    Painting.save(request.form)
    return redirect('/paintings')

# TODO READ ALL
@app.route('/paintings')
def paintings():
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template("paintings.html",paintings=Painting.get_all_with_users())

# TODO READ ONE
@app.route('/painting/show/<int:id>')
def show_paintings(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data ={ 
        "id":id
    }
    return render_template("show_painting.html",painting=Painting.get_one_with_user(data))

# ! ///// UPDATE /////
# TODO UPDATE REQUIRES TWO ROUTES
# TODO ONE TO SHOW THE FORM
@app.route('/painting/edit/<int:id>')
def edit_painting(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data ={ 
        "id":id
    }
    return render_template("edit_painting.html",painting=Painting.get_one(data))

# TODO ONE TO HANDLE THE DATA FROM THE FORM
@app.route('/painting/update',methods=['POST'])
def update_painting():
    Painting.update(request.form)
    return redirect('/paintings')

# ! ///// DELETE //////
@app.route('/painting/destroy/<int:id>')
def destroy_painting(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': id
    }
    Painting.destroy(data)
    return redirect('/paintings')