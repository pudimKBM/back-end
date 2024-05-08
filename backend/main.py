from flask import Flask, request
from app.database.database import init_db
from app.database.database import db
from app.routers import auth_router, data_router, batch_router
from os import environ
from flask_jwt_extended import JWTManager, get_jwt_identity, jwt_required
from app.utils.log_utils import setup_logger
from flask_jwt_extended import get_jwt

app = Flask(__name__)
# app.config['SECRET_KEY'] = environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
app.config['JWT_SECRET_KEY'] = environ.get('JWT_SECRET_KEY')
logger = setup_logger('request_logger', 'requests.log')

@app.before_request
@jwt_required(optional=True)  # Make JWT optional for this endpoint
def log_request_info():
    """Log information about incoming requests"""
    ip_address = request.remote_addr
    jwt_token = None
    try:
        jwt_token = get_jwt()
    except Exception as e:
        pass
    logger.info(f'IP: {ip_address}, Path: {request.path}, Method: {request.method}, JWT Token: {jwt_token}, Body: {request.get_data(as_text=True)}')

@app.after_request
def log_response_info(response):
    """Log information about outgoing responses"""
    logger.info(f'Response: {response.status_code}')
    return response

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
    app.run(host="127.0.0.1", port=8000)
