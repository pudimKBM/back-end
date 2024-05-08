from flask import Flask  
from app.database.database import init_db
from app.database.database import db
from app.routers import auth_router, data_router, batch_router  
from os import environ
from flask_jwt_extended import JWTManager
  
app = Flask(__name__)
# app.config['SECRET_KEY'] = environ.get('SECRET_KEY')  
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')  
app.config['JWT_SECRET_KEY'] = "BgfkMsRj0svlfz_Ka2WZ-kduGPnGQH1Eqqv4XgFRRns"

jwt = JWTManager(app)
# Initialize Database  
init_db(app)  
  
# Register Blueprints  
app.register_blueprint(auth_router.auth_bp)  
app.register_blueprint(data_router.data_bp)  
app.register_blueprint(batch_router.batch_bp)
with app.app_context():  
    db.create_all()
  
if __name__ == "__main__":  
    # import uvicorn  
    # uvicorn.run(app, host="127.0.0.1", port=8000)
    app.run(host="127.0.0.1", port=8000)