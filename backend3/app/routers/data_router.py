from flask import Blueprint, request, jsonify  
from sqlalchemy.exc import IntegrityError  
from app.database.database import db  
from app.models.models import CardInfo  
from app.schemas.schemas import CardInfoSchema  
from app.utils.crypto_utils import encrypt_data, decrypt_data
from flask_jwt_extended import jwt_required  
  
data_bp = Blueprint('data_bp', __name__)  
  
@data_bp.route('/card', methods=['POST'])  
@jwt_required()
def insert_card():  
    card_data = request.json  
    card_schema = CardInfoSchema(**card_data)  
    encrypted_card_number = encrypt_data(card_schema.card_number)  
    new_card = CardInfo(card_number=encrypted_card_number)  
    db.session.add(new_card)  
    try:  
        db.session.commit()  
    except IntegrityError:  
        return jsonify({"error": "Card number might already exist."}), 400  
    return jsonify({"message": "Card data inserted successfully."}), 201  
  
@data_bp.route('/card/<card_number>', methods=['GET'])
@jwt_required() 
def get_card(card_number):  
    encrypted_card_number = encrypt_data(card_number)  
    card_info = CardInfo.query.filter_by(card_number=encrypted_card_number).first()  
    if card_info:  
        decrypted_card_number = decrypt_data(card_info.card_number)  
        return jsonify({"card_number": decrypted_card_number}), 200  
    else:  
        return jsonify({"error": "Card number not found."}), 404  