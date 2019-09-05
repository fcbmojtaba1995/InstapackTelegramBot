import requests
import json
from flask import Flask, request, Response

app = Flask(__name__)


def write_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    app.run(debug=True)
