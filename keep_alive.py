from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "✅ Klipso's private bot is alive on Railway!"

def run():
    app.run(host='0.0.0.0', port=3000)

def keep_alive():
    t = Thread(target=run)
    t.start()
