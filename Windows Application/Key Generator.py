from cryptography.fernet import Fernet

def generate_key():
    """Generate a random encryption key."""
    return Fernet.generate_key()

def encrypt_file(filename, key):
    """Encrypt the contents of a file using the provided key."""
    cipher_suite = Fernet(key)
    with open(filename, 'rb') as file:
        plaintext = file.read()
    encrypted_data = cipher_suite.encrypt(plaintext)
    with open(filename + '.encrypted', 'wb') as encrypted_file:
        encrypted_file.write(encrypted_data)

def decrypt_file(encrypted_filename, key):
    """Decrypt the contents of an encrypted file using the provided key."""
    cipher_suite = Fernet(key)
    with open(encrypted_filename, 'rb') as encrypted_file:
        encrypted_data = encrypted_file.read()
    decrypted_data = cipher_suite.decrypt(encrypted_data)
    decrypted_filename = encrypted_filename.replace('.encrypted', '.decrypted')
    with open(decrypted_filename, 'wb') as decrypted_file:
        decrypted_file.write(decrypted_data)

# Example usage:
key = generate_key()
source_file = 'plaintext.txt'
encrypt_file(source_file, key)
encrypted_file = source_file + '.encrypted'
decrypt_file(encrypted_file, key)
