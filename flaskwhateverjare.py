from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

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
                search_results.append(url)
        return search_results
    except requests.exceptions.RequestException:
        return []

@app.route('/', methods=['GET'])
def index():
    return render_template('query_form.html')

@app.route('/process_query', methods=['POST'])
def process_query():
    query = request.form.get('query')
    #print(query)
    links = search_google(query)
    # num_links = len(links)
    
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
    return content

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
