from flask import Blueprint, request, jsonify  
from werkzeug.utils import secure_filename  
from app.database.database import db  
from app.models.models import CardInfo  
from app.utils.crypto_utils import encrypt_data, generate_token 
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
import json
  
batch_bp = Blueprint('batch_bp', __name__)  
  
@batch_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_file():
    current_user = get_jwt_identity()
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        try:
            process_file(file, current_user)
            return jsonify({"message": "File processed successfully."}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Invalid file type."}), 400

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'txt'

from sqlalchemy.exc import IntegrityError

def process_file(file, current_user):
    secure_filename(file.filename)  
    lines = file.readlines()[:-1]
    batch_info = {}
    processed_cards = set()  
    first_line_processed = False 
    for line in lines:
        line = line.decode('utf-8').strip()
        if not first_line_processed:
            batch_info['name'] = line[0:29].strip()
            batch_info['date'] = str(datetime.strptime(line[30:37], '%Y%m%d'))
            batch_info['batch_number'] = line[37:45]
            batch_info['record_count'] = int(line[46:51])
            first_line_processed = True 
            continue 
        if line.startswith('C'):
            card_number = line[7:].strip()
            if len(card_number) != 16 :
                print(card_number)
                continue 
            encrypted_card_number = encrypt_data(card_number)  
            card_number_token = generate_token(card_number)
        
            if card_number in processed_cards:
                continue  
            
            existing_card = CardInfo.query.filter_by(card_number=encrypted_card_number).first()
            if existing_card:
                processed_cards.add(card_number) 
                continue  
            new_card = CardInfo(
                card_number=encrypted_card_number,
                card_number_token=card_number_token,
                user_added=current_user,
                card_metadata=json.dumps(batch_info)
            )
            try:
                db.session.add(new_card)
                db.session.commit()
                processed_cards.add(card_number)  
            except IntegrityError as e:
                db.session.rollback()
                print(f"Error inserting card number {card_number}: {e}")
            except Exception as e:
                db.session.rollback()
                print(f"Unexpected error: {e}")
