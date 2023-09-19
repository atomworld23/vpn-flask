from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup
from cryptography.fernet import Fernet

app = Flask(__name__)

# Generate a secret key for encryption (This should be securely managed in practice)
secret_key = Fernet.generate_key()
cipher_suite = Fernet(secret_key)

def encrypt_query(query):
    encrypted_query = cipher_suite.encrypt(query.encode())
    return encrypted_query

def decrypt_query(encrypted_query):
    decrypted_query = cipher_suite.decrypt(encrypted_query).decode()
    return decrypted_query

# ... rest of your code ...

@app.route('/process_query', methods=['POST'])
def process_query():
    query = request.form.get('query')
    encrypted_query = encrypt_query(query)  # Encrypt the query
    
    links = search_google(encrypted_query)  # Pass encrypted query to search function
    
    return render_template("response.html", links=links, link_base='/handlelinks?url=')

@app.route("/handlelinks")
def handle_extlink():
    link = request.args.get("url")
    
    user_ip = request.remote_addr  # Get the user's IP address
    
    try:
        response = requests.get(link)
        response.raise_for_status()
        content = response.text
    except requests.exceptions.RequestException:
        content = "404"
    print(f"User IP: {user_ip}")  # Print the user's IP address in the terminal
    decrypted_query = decrypt_query(request.args.get("query"))  # Decrypt the query
    print(f"Decrypted Query: {decrypted_query}")  # Print the decrypted query
    return content

# ... rest of your code ...
