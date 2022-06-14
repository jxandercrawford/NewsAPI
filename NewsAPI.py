import flask
from flask import request

from News import *
from apiMethods import *

# Initialize app
app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Home page
@app.route('/', methods=['GET'])
def home():
    return '''
    <h1>Xander's News RSS API</h1>
    <p>Get the lastest stories here!</p>
    '''

# NYT page
@app.route('/api/nyt', methods=['GET'])
def api_nyt():

    return api_news(NYT(), "json")

# WSJ page
@app.route('/api/wsj', methods=['GET'])
def api_wsj():

    return api_news(WSJ(), "json")

if __name__ == "__main__":
    app.run()
