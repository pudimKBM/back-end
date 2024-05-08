from flask import Blueprint,request, jsonify  
from app.models.models import User  
from app.database.database import db
from app.schemas.schemas import UserValidateSchema  

from flask_jwt_extended import create_access_token  
from datetime import timedelta, datetime, timezone
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    try:  
        data = UserValidateSchema(**request.get_json())
        mail = data.mail  
        password = data.password   
        if mail is None or password is None:  
            return jsonify({"message": "Missing username or password"}), 400  
        if User.query.filter_by(mail=mail).first() is not None:  
            return jsonify({"message": "User already exists"}), 400  
        user = User(mail=mail)  
        user.set_password(password)  
        db.session.add(user)  
        db.session.commit()  
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e :
        print(e)

  
@auth_bp.route('/login', methods=['POST'])  
def login():  
    data = UserValidateSchema(**request.get_json())
    mail = data.mail  
    password = data.password   
    user = User.query.filter_by(mail=mail).first()  
    if user is None or not user.check_password(password):  
        return jsonify({"message": "Invalid username or password"}), 401  

    # Update the date_modified column with the current date and time
    user.date_modified = datetime.now(timezone.utc)

    # Commit the changes to the database
    db.session.commit()

    # Generate access token
    access_token = create_access_token(identity=mail, expires_delta=timedelta(days=1))  

    return jsonify(access_token=access_token), 200  