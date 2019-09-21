import requests
import json
from flask import Flask, request, Response
import config as db_config

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        msg = request.get_json()

        return Response('ok', status=200)

    else:
        return '<h1>Insta Pack Telegram Bot</h1>'


if __name__ == '__main__':
    db_config.connect_to_database()
    # app.run(debug=True)
