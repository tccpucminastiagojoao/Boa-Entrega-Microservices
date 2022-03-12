from flask import Flask, jsonify, make_response, request
import requests


app = Flask(__name__)


@app.route('/clientes', methods=['GET'])
def clientes():
    return make_response(jsonify({'message': 'Hello from mic-sic-microservice'}), 200)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
