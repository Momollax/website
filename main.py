from flask import Flask, request, redirect, url_for, render_template_string
import requests
from flask import Flask, render_template
from flask import Flask, send_from_directory
app = Flask(__name__)

# Fonction pour récupérer les informations sur l'adresse IP à partir de l'API
def get_ip_info(ip):

    # Remplacez cette ligne par ip = request.remote_addr pour obtenir l'adresse IP du client
    try:
        response = requests.get('http://ip-api.com/json/' + str(ip))
        return response.json()
    except Exception as e:
        print('Erreur lors de la récupération de l\'adresse IP :', str(e))
        return None

# Envoi de la notification Discord via le webhook
def send_discord_notification(url, ip, status):
    ip_info = get_ip_info(ip)
    user_agent = request.headers.get('User-Agent')
    try:
        latitude = ip_info['lat']
        longitude = ip_info['lon']
        google_maps_link = f"https://www.google.com/maps?q={latitude},{longitude}"
        message = f"IP: {ip} access {url}. Status: {status}.User-Agent: {user_agent} - {ip_info['country']}, {ip_info['city']}, {ip_info['isp']}. [Google Maps]({google_maps_link})"
    except:
        message = f"IP: {ip} access {url}. Status: {status}.User-Agent: {user_agent} "

    webhook_url = 'https://discord.com/api/webhooks/1214330961240789012/NJ2Mb4-ZHnLGYgAyiEzBE6m7Jv5qTk8DoVjefiFWzeAPSa5HuIfHw9GUTRB-gHZ14YGJ'
    try:
        #response = requests.post(webhook_url, json={"content": message})
        print('Notification Discord envoyée avec succès')
    except Exception as e:
        print('Erreur lors de l\'envoi de la notification Discord :', str(e))

# Middleware pour intercepter le statut de la réponse
@app.after_request
def after_request(response):
    url = request.full_path
    ip = request.remote_addr
    status = response.status_code
    #send_discord_notification(url, ip, status)
    return response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/git')
@app.route('/git.html')
def git():
    return render_template('git.html')

@app.route('/.well-known/gpg_key.txt')
def security():
    return render_template('gpg_key.txt')

@app.route('/cv')
@app.route('/cv.html')
def cv():
    return render_template('cv.html')

@app.route('/cv2')
@app.route('/cv2.html')
def cv2():
    return render_template('cv2.html')

@app.route('/writeup')
@app.route('/writeup.html')
def writeup():
    return render_template('writeup.html')

if __name__ == '__main__':
    app.run(port=1234)
