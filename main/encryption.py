from dotenv import set_key
from cryptography.fernet import Fernet

def generate_keys():
    user_key = Fernet.generate_key()
    set_key(".env", "user_crypt_key", user_key.decode())

    script_key = Fernet.generate_key()
    set_key(".env", "script_crypt_key", script_key.decode())
            
    token_key = Fernet.generate_key()
    set_key(".env", "token_crypt_key", token_key.decode())


#example
message = b"Hello, this is a secret message!"

cipher_suite = Fernet("clé à inserer")
encrypted_message = cipher_suite.encrypt(message)