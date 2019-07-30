from flask import Flask, jsonify

from flaskr.services import get_spaceship_data


app = Flask(__name__)


@app.route('/', methods=['GET'])
def spaceships():
    return jsonify(get_spaceship_data())


if __name__ == "__main__":
    app.run(debug=True)
