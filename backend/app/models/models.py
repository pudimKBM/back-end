from app.database.database import db  
from sqlalchemy import Column, String, Integer, DateTime, func, JSON
from werkzeug.security import generate_password_hash, check_password_hash  
  
class CardInfo(db.Model):  
    __tablename__ = 'card_info'  
      
    id = Column(Integer, primary_key=True)  
    card_number = Column(String, unique=True, nullable=False)
    card_number_token = Column(String, unique=True, nullable=False)
    user_added = Column(String, nullable=False)
    date_created = Column(DateTime, default=func.now())
    date_modified = Column(DateTime, default=func.now(), onupdate=func.now())
    card_metadata =  Column(JSON,nullable=True)
  
  
class User(db.Model):  
    __tablename__ = 'users'  
      
    id = Column(Integer, primary_key=True)
    mail = Column(String, index=True, unique=True, nullable=False)  
    password_hash = Column(String)
    date_created = Column(DateTime, default=func.now())
    date_modified = Column(DateTime, default=func.now(), onupdate=func.now())
    

    def __repr__(self):  
        return f"<User date_created={self.date_created}, date_modified={self.date_modified}>"
    def set_password(self, password):  
        self.password_hash = generate_password_hash(password)  
  
    def check_password(self, password):  
        return check_password_hash(self.password_hash, password) 