from flask import Flask
from flask import request

app = Flask(__name__)


@app.route('/webhook', methods=['POST', 'GET'])
def webhook():
    """ main agent
    """
    respone = request.get_json(force=True)
    return respone
