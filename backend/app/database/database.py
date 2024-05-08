from flask_sqlalchemy import SQLAlchemy  
from sqlalchemy import create_engine  
from sqlalchemy.orm import scoped_session, sessionmaker  
from dotenv import load_dotenv  
import os  
  
load_dotenv()  
DATABASE_URL = os.getenv("DATABASE_URL")  
  
engine = create_engine(DATABASE_URL)  
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))  
  
db = SQLAlchemy()  
  
def init_db(app):  
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL  
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)  