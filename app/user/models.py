from flask import Flask, jsonify, request, session
from werkzeug.utils import redirect
from passlib.hash import pbkdf2_sha256
from app import db
from datetime import date
import uuid


class User:

    def start_session(self, user):
        del user['password']
        session['logged_in'] = True
        session['user'] = user
        

    def signup(self):
        user = {
            "_id": uuid.uuid4().hex,
            "name": request.form.get('name'),
            "email": request.form.get('email').lower(),
            "password": request.form.get('password')
        }

        user['password'] = pbkdf2_sha256.hash(user['password'])
    
        if db.users.find_one({'email': user['email'] }):
            return jsonify({'error': 'Email address already in use'}), 400

        if db.users.insert_one(user):
            self.start_session(user)
            return user, 200

        return jsonify({'error': 'Signup failed'}), 400


    def signout(self):
        session.clear()
        return redirect('/')

    
    def login(self):
        user = db.users.find_one({'email': request.form.get('email')})

        if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
            self.start_session(user)
            return user, 200
        
        return jsonify({'error': 'Invalid login credentials'}) , 400


