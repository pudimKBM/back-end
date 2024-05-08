from cryptography.fernet import Fernet  
import os  
import hashlib  
 
encryption_key = os.getenv('ENCRYPTION_KEY')
cipher_suite = Fernet(encryption_key)  
  
def encrypt_data(data: str) -> str:  
    return cipher_suite.encrypt(data.encode()).decode()  
  
def decrypt_data(data: str) -> str:
    return cipher_suite.decrypt(data.encode()).decode()  

def generate_token(data: str) -> str:  
    return hashlib.sha256(data.encode()).hexdigest()