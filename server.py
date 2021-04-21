# # 3 - create routes

# make an account

# filter by __

# add donations / resources (into resources table)

# display map

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db
import crud
from jinja2 import StrictUndefined


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined



@app.route('/')
def homepage():
    return render_template('homepage.html')



@app.route('/login', methods=['GET', 'POST'])
def sign_in():
    """Sign in to user account"""

    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')
        user_in_db = crud.confirm_current_user(username)

        if user_in_db == False:
            flash('No account with that username, please try again or create an account')
            return render_template('login.html')

        else:
            user = crud.find_user_by_username(username)
            
            if password == user.password:
                session['user_id'] = user.user_id
                return render_template('homepage.html') 
            
            else:
                flash('Incorrect password')
                return render_template('login.html')

    if request.method == 'GET':

        return render_template('login.html')



@app.route('/logout')
def log_out():
    """Log out of account."""

    session.pop('user_id', None)
    return redirect('/')
   


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    """Create an account."""
    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        city = request.form.get('city')
        state = request.form.get('state')

        user_in_db = crud.confirm_current_user(username)

        if user_in_db == False:

            user =  crud.create_user(username, password, email, city, state)
            session['user_id'] = user.user_id
            flash('Account Creation Complete; you can now contribute to Resources')
            return render_template('homepage.html')

        else:
            flash('Already an account for that username, please login')
            return render_template('login.html') 

        return render_template('homepage.html')
    
    if request.method == 'GET':
        return render_template('sign_up.html')



@app.route('/create_orgs', methods=['GET', 'POST'])
def create_orgs():
    """Add a resource or organization to the db."""
    if request.method == 'POST':

        org_name = request.form.get('org_name')
        url = request.form.get('url')
        email = request.form.get('email')
        phone = request.form.get('phone')
        city = request.form.get('city')
        state = request.form.get('state')

        org_in_db = crud.confirm_current_org(org_name)

        if org_in_db == False:

            org = crud.create_org(org_name, url, email, phone, city, state, user_id=session['user_id'])
            session['org_id'] = org.org_id
            flash('Organization has been added to the resources')
            return redirect('/resources')

        else:
            flash('That organization is already in the resources')
            return redirect('/resources') 
    
    if request.method == 'GET':
        return redirect('/resources')



@app.route('/resources', methods=['POST', 'GET'])
def all_resources():
    """Return all resources entered by users."""
    
    show_resources = crud.list_resources()

    return render_template('resources.html', show_resources = show_resources)






if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)