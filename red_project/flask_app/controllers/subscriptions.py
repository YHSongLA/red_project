from flask import render_template, request, redirect, session
from flask_app import app
from flask_app.models.subscription import Subscription

# ! ////// CREATE  //////
# TODO CREATE REQUIRES TWO ROUTES:
# TODO ONE TO DISPLAY THE FORM:
@app.route('/subscription/new')
def new_subscription():
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template("new_subscription.html")

# TODO ONE TO HANDLE THE DATA FROM THE FORM
@app.route('/subscription/create',methods=['POST'])
def create_subscription():
    print(request.form)
    Subscription.save(request.form)
    return redirect('/subscriptions')

# TODO READ ALL
@app.route('/subscriptions')
def subscriptions():
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template("subscriptions.html",subscriptions=Subscription.get_all_with_users())

# TODO READ ONE
@app.route('/subscription/show/<int:id>')
def show_subscriptions(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data ={ 
        "id":id
    }
    return render_template("show_subscription.html",subscription=Subscription.get_one_with_user(data))

# ! ///// UPDATE /////
# TODO UPDATE REQUIRES TWO ROUTES
# TODO ONE TO SHOW THE FORM
@app.route('/subscription/edit/<int:id>')
def edit_subscription(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data ={ 
        "id":id
    }
    return render_template("edit_subscription.html",subscription=Subscription.get_one(data))

# TODO ONE TO HANDLE THE DATA FROM THE FORM
@app.route('/subscription/update',methods=['POST'])
def update_subscription():
    Subscription.update(request.form)
    return redirect('/subscriptions')

# ! ///// DELETE //////
@app.route('/subscription/destroy/<int:id>')
def destroy_subscription(id):
    data ={
        'id': id
    }
    print('*'*20)
    print(data)
    print('*'*20)
    Subscription.destroy(data)
    return redirect(f"/users/edit/{session['user_id']}")