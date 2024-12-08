from flask import Flask
from flask_sqlalchemy import SQLAlchemy


from dotenv import load_dotenv
from cryptography.fernet import Fernet
import os


# Load environment variables from .env file
load_dotenv()

# Access the AES key
AES_KEY = os.getenv('NOT_MY_KEY')


app = Flask(__name__)

# Your database setup and configuration here
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yourdatabase.db'
db = SQLAlchemy(app)

# Get encryption key from environment variable
key = os.getenv('NOT_MY_KEY')

if not key:
    # If the environment variable is not set, raise an error
    raise ValueError("Encryption key (NOT_MY_KEY) is not set in the environment variables.")

# Initialize the Fernet cipher using the encryption key
fernet = Fernet(key)


# Define your models here
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

# Create tables (this should be inside the app context)
with app.app_context():
    db.create_all()

# Now you can start your application
if __name__ == "__main__":
    app.run(debug=True)

# Function to encrypt a private key
def encrypt_private_key(private_key: str) -> str:
    # Ensure the private key is in bytes
    private_key_bytes = private_key.encode()
    encrypted_key = fernet.encrypt(private_key_bytes)
    return encrypted_key.decode()  # Convert back to string for storage

# Function to decrypt a private key
def decrypt_private_key(encrypted_private_key: str) -> str:
    encrypted_key_bytes = encrypted_private_key.encode()
    decrypted_key = fernet.decrypt(encrypted_key_bytes)
    return decrypted_key.decode()  # Return as string
# Database model for a Private Key (e.g., JWKS private key)
class PrivateKey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    encrypted_key = db.Column(db.String(255), nullable=False)

# Create tables
with app.app_context():
    db.create_all()
# Example of encrypting a private key before storing it
private_key = "mysecretprivatekey"
encrypted_key = encrypt_private_key(private_key)

# Create a new entry in the PrivateKey table
new_key = PrivateKey(name="my_private_key", encrypted_key=encrypted_key)

with app.app_context():
    db.session.add(new_key)
    db.session.commit()
# Example of retrieving and decrypting a private key from the database
stored_key = PrivateKey.query.filter_by(name="my_private_key").first()
decrypted_key = decrypt_private_key(stored_key.encrypted_key)
print(f"Decrypted Private Key: {decrypted_key}")

export NOT_MY_KEY="your_super_secret_key"
