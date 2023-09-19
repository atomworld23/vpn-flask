from flask import Flask,request,render_template
import requests
from bs4 import BeautifulSoup
from cryptography.fernet import Fernet

app = Flask(__name__)

#generating a random key for encryption
encrypt_key = Fernet.generate_key()
cipher_suite = Fernet(encrypt_key)

#generating a google search query
def search_google(query):
    search_results = []
    try:
        response = requests.get(f"https://www.google.com/search?q={query}")
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a')
        for link in links:
            href = link.get('href')
            if href and href.startswith('/url?q='):
                url = href.split('/url?q=')[1].split('&')[0]
                encrypted_url = cipher_suite.encrypt(url.encode()).decode()
                search_results.append(encrypted_url)
        return search_results
    except requests.exceptions.RequestException:
        return []

@app.route('/', methods = ['GET'])
def index():
    return render_template('response.html')

@app.route('/process_query', methods =['POST'])
def process_query():
    query = request.form.get('query')
    links = search_google(query)

    return render_template("response.html", links=links, link_base ='/handlelinks?url=')

@app.route("/handlelinks")
def handle_extlink():
    encrypted_link = request.args.get("url")
    decrypted_url = cipher_suite.decrypt(encrypted_link.encode()).decode()

    user_ip = request.remote_addr

    try:
        response = requests.get(decrypted_url)
        response.raise_for_status()
        content = response.text
    except requests.exceptions.RequestException:
        content = "404"

    print(f"User IP: {user_ip}")
    return content 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)