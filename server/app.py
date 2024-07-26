from flask import request, session
from flask_restful import Resource
from config import app, db, api
from models import User

class Signup(Resource):
    def post(self):
        data = request.json
        username = data.get('username')
        password = data.get('password')

        if User.query.filter_by(username=username).first():
            return {'error': 'Username already exists'}, 400

        user = User(username=username)
        user.password_hash = password  
        
        db.session.add(user)
        db.session.commit()
        
        session['user_id'] = user.id
        
        return user.to_dict(), 201

class Login(Resource):
    def post(self):
        data = request.json
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()
        
        if user and user.authenticate(password):
            session['user_id'] = user.id
            return user.to_dict(), 200
        
        return {'error': 'Invalid username or password'}, 401

class Logout(Resource):
    def delete(self):
        session.pop('user_id', None)
        return {}, 204

class CheckSession(Resource):
    def get(self):
        user_id = session.get('user_id')
        if user_id:
            user = User.query.get(user_id)
            if user:
                return user.to_dict(), 200
        return {}, 204

api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(CheckSession, '/check_session')

if __name__ == '__main__':
    app.run(port=5555, debug=True)