from flask import Blueprint, request, jsonify  
from sqlalchemy.exc import IntegrityError  
from app.database.database import db  
from app.models.models import CardInfo  
from app.schemas.schemas import CardInfoSchema  
from app.utils.crypto_utils import encrypt_data, decrypt_data, generate_token
from flask_jwt_extended import jwt_required, get_jwt_identity
import json
  
data_bp = Blueprint('data_bp', __name__)  
  
@data_bp.route('/card', methods=['POST'])  
@jwt_required()
def insert_card():
    current_user = get_jwt_identity()
    card_data = request.json  
    card_schema = CardInfoSchema(**card_data)  
    encrypted_card_number = encrypt_data(card_schema.card_number)  
    card_number_token = generate_token(card_schema.card_number)
    new_card = CardInfo(card_number=encrypted_card_number,
                        card_number_token=card_number_token,
                        user_added=current_user)
    db.session.add(new_card)  
    try:  
        db.session.commit()  
    except IntegrityError:  
        return jsonify({"error": "Card number might already exist."}), 400  
    return jsonify({"message": "Card data inserted successfully."}), 201  
  
@data_bp.route('/card/<card_number>', methods=['GET'])
@jwt_required() 
def get_card(card_number):  
    card_number_token = generate_token(card_number)
    card_info = CardInfo.query.filter_by(card_number_token=card_number_token).first()  
    if card_info:  
        decrypted_card_number = decrypt_data(card_info.card_number)  
        return jsonify({"card_number": decrypted_card_number,
                        "date_created":card_info.date_created,
                        "user_added":card_info.user_added,
                        "metadata":json.loads(card_info.card_metadata)}), 200  
    else:  
        return jsonify({"error": "Card number not found."}), 404  