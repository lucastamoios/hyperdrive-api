from flask import Flask, jsonify


starships = [
    {
        'name': 'Naboo star skiff',
        'hyperdrive': '0.5'
    }
]


app = Flask(__name__)


@app.route('/', methods=['GET'])
def spaceships():
    return jsonify(starships)


if __name__ == "__main__":
    app.run(debug=True)
