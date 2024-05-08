from flask import Blueprint,request, jsonify  
from app.models.models import User  
from app.database.database import db

from flask_jwt_extended import create_access_token  
from datetime import timedelta  
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])  
def register():
    try:
        data = request.get_json()  
        username = data.get('username')  
        password = data.get('password')  
        if username is None or password is None:  
            return jsonify({"message": "Missing username or password"}), 400  
        if User.query.filter_by(username=username).first() is not None:  
            return jsonify({"message": "User already exists"}), 400  
        user = User(username=username)  
        user.set_password(password)  
        db.session.add(user)  
        db.session.commit()  
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e :
        print(e)

  
@auth_bp.route('/login', methods=['POST'])  
def login():  
    data = request.get_json()  
    username = data.get('username')  
    password = data.get('password')  
    user = User.query.filter_by(username=username).first()  
    if user is None or not user.check_password(password):  
        return jsonify({"message": "Invalid username or password"}), 401  
    access_token = create_access_token(identity=username, expires_delta=timedelta(days=1))  
    return jsonify(access_token=access_token), 200  