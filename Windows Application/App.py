import tkinter as tk
from tkinter import filedialog
from cryptography.fernet import Fernet

def generate_key():
    key = Fernet.generate_key()
    print(key)
    return key

def encrypt_file(filename, key):
    cipher_suite = Fernet(key)
    with open(filename, 'rb') as file:
        plaintext = file.read()
    encrypted_data = cipher_suite.encrypt(plaintext)
    with open(filename + '.encrypted', 'wb') as encrypted_file:
        encrypted_file.write(encrypted_data)

def decrypt_file(encrypted_filename, key):
    cipher_suite = Fernet(key)
    with open(encrypted_filename, 'rb') as encrypted_file:
        encrypted_data = encrypted_file.read()
    decrypted_data = cipher_suite.decrypt(encrypted_data)
    decrypted_filename = encrypted_filename.replace('.encrypted', '.decrypted')
    with open(decrypted_filename, 'wb') as decrypted_file:
        decrypted_file.write(decrypted_data)

def select_file():
    global filename
    filename = filedialog.askopenfilename()
    file_entry.delete(0, tk.END)
    file_entry.insert(0, filename)

def encrypt():
    key = generate_key()
    encrypt_file(filename, key)
    status_label.config(text="File Encrypted")

def decrypt():
    encrypted_filename = filename + '.encrypted'
    key = input("Enter your encryption key: ")  # You need to store and retrieve the key securely
    decrypt_file(encrypted_filename, key)
    status_label.config(text="File Decrypted")

root = tk.Tk()
root.title("File Encryptor")

file_label = tk.Label(root, text="Select File:")
file_label.pack()

file_entry = tk.Entry(root, width=50)
file_entry.pack()

select_button = tk.Button(root, text="Browse", command=select_file)
select_button.pack()

encrypt_button = tk.Button(root, text="Encrypt", command=encrypt)
encrypt_button.pack()

decrypt_button = tk.Button(root, text="Decrypt", command=decrypt)
decrypt_button.pack()

status_label = tk.Label(root, text="")
status_label.pack()

root.mainloop()
