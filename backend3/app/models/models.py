from app.database.database import db  
from sqlalchemy import Column, String, Integer  
from werkzeug.security import generate_password_hash, check_password_hash  
  
class CardInfo(db.Model):  
    __tablename__ = 'card_info'  
      
    id = Column(Integer, primary_key=True)  
    card_number = Column(String, unique=True, nullable=False)  
    # Ensure to encrypt this field with cryptography before saving  
  
    def __repr__(self):  
        return f"<CardInfo {self.card_number}>"
  
class User(db.Model):  
    __tablename__ = 'users'  
      
    id = db.Column(db.Integer, primary_key=True)  
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)  
    password_hash = db.Column(db.String(128))  
  
    def set_password(self, password):  
        self.password_hash = generate_password_hash(password)  
  
    def check_password(self, password):  
        return check_password_hash(self.password_hash, password) 