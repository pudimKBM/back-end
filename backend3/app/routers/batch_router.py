from flask import Blueprint, request, jsonify  
from werkzeug.utils import secure_filename  
from app.database.database import db  
from app.models.models import CardInfo  
from app.utils.crypto_utils import encrypt_data  
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required  
  
batch_bp = Blueprint('batch_bp', __name__)  
  
@batch_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_file():  
    if 'file' not in request.files:  
        return jsonify({"error": "No file part"}), 400  
    file = request.files['file']  
    if file.filename == '':  
        return jsonify({"error": "No selected file"}), 400  
    if file and allowed_file(file.filename):  
        try:  
            process_file(file)  
            return jsonify({"message": "File processed successfully."}), 200  
        except Exception as e:  
            return jsonify({"error": str(e)}), 500  
    else:  
        return jsonify({"error": "Invalid file type."}), 400  
  
def allowed_file(filename):  
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'txt'  
  
def process_file(file):  
    secure_filename(file.filename)  # Ensure the filename is secure  
    lines = file.readlines()  
    for line in lines:  
        process_line(line.decode('utf-8').strip())  
  
def process_line(line):  
    if line.startswith('C'):  
        card_number = line[7:23].strip()  # Adjust indices based on your file format  
        encrypted_card_number = encrypt_data(card_number)  
        new_card = CardInfo(card_number=encrypted_card_number)  
        db.session.add(new_card)  
    try:  
        db.session.commit()  
    except IntegrityError:  
        db.session.rollback()  # Rollback in case of an error to avoid blocking other transactions  
