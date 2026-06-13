import bcrypt
from flask import render_template, redirect, request, url_for, session
from app import db

def home():
    return render_template('index.html')

def dashboard():
    if "email" in session:
        return render_template('dashboard.html')
    else:
        return redirect(url_for('auth.login'))

def settings():
    if request.method == "GET":
        return render_template('settings.html')
    else:
        collection = db['users']
        form_data = request.form
        query_data = {
            "email": form_data['email']
        }
        result = collection.find_one(query_data)
        response = ''
        if result and bcrypt.checkpw(form_data['current_password'].encode('utf-8'), result['password'].encode('utf-8')):
            hashed_password = bcrypt.hashpw(form_data['new_password1'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            update_data = {
                "name": form_data['name'],
                "password": hashed_password,
            }
            result = collection.find_one_and_update(query_data, { "$set" : update_data })
            if result:
                response = 'succeeded'
                session['name'] = form_data['name']
        else:
            response = 'failed'
        return render_template('settings.html', response=response)
       

def contact_us():
    return render_template('contactUs.html')

def services():
    return render_template('services.html')