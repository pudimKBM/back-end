from cryptography.fernet import Fernet  
import os  

# Ideally, the key should be securely fetched from an environment variable or a secure vault.  
encryption_key = os.environ.get('ENCRYPTION_KEY') 
cipher_suite = Fernet(encryption_key)  
  
def encrypt_data(data: str) -> str:  
    return cipher_suite.encrypt(data.encode()).decode()  
  
def decrypt_data(data: str) -> str:  
    return cipher_suite.decrypt(data.encode()).decode()  