from flask import Flask, jsonify, make_response, request
import os
import sys
import requests
import numbers
import string
import random
from datetime import datetime, timedelta
from dateutil import parser


# Postgres configuration
POSTGRES_DB = os.environ['POSTGRES_DB']
POSTGRES_USER = os.environ['POSTGRES_USER']
POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD']
POSTGRES_SERVICE = os.environ['POSTGRES_SERVICE']

# Api Gateway configuration
API_GATEWAY = os.environ['API_GATEWAY']
API_GATEWAY_URL = 'http://{0}:80'.format(API_GATEWAY)
API_GATEWAY_JSON_HEADERS = {'accept': 'application/json',
                            'content-type': 'application/json'}
API_GATEWAY_AUTH = None


def get_api_gateway(req_url, req_params={}):
    try:
        api_gateway_req_url = '{0}{1}'.format(API_GATEWAY_URL, req_url)
        print("API Gateaway request GET:",
              api_gateway_req_url, "Parameters:", req_params)
        req_res = requests.get(
            url=api_gateway_req_url, headers=API_GATEWAY_JSON_HEADERS, auth=API_GATEWAY_AUTH, params=req_params)
        req_res_json = req_res.json()

        # Avoid json conversion to a number (need to convert to string)
        if (isinstance(req_res_json, numbers.Number)):
            req_res_json = str(req_res_json)

        return req_res_json, req_res.status_code
    except requests.exceptions.JSONDecodeError:
        req_res_text = req_res.text
        return req_res_text, req_res.status_code
    except requests.exceptions.ConnectionError:
        req_res_error = 'Failed to establish a connection: {0}{1}'.format(
            API_GATEWAY_URL, req_url)
        return req_res_error, 503


def create_app():
    """
    Application factory
    """
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{0}:{1}@{2}:5432/{3}'.format(
        POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_SERVICE, POSTGRES_DB)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from models import db
    db.init_app(app)
    with app.app_context():
        db.drop_all()  # Only for tests with data examples
        db.create_all()
        db.session.commit()

    from models import Indicador
    with app.app_context():
        # Populate Clientes with examples
        if Indicador.query.count() == 0:
            db.session.add(Indicador(nome="Indicador 1",
                           data_criacao=datetime.now()))
            db.session.add(Indicador(nome="Indicador 2",
                           data_criacao=datetime.now()))
            db.session.add(Indicador(nome="Indicador 3",
                           data_criacao=datetime.now()))
            db.session.commit()

    @app.route('/indicadores', methods=['GET'])
    def clientes():
        indicadores = db.session.query(Indicador).all()
        return make_response(jsonify(indicadores), 200)

    @app.route('/indicadores/<int:indicador_id>', methods=['GET'])
    def get_cliente(indicador_id):
        indicador = db.session.query(Indicador).get(indicador_id)
        if indicador:
            return make_response(jsonify(indicador), 200)
        else:
            return make_response(jsonify({'message': 'Indicador Not Found'}), 404)

    @app.route('/indicadores/pedidos', methods=['GET'])
    def get_pedidos():
        # Retrieve pedidos completed
        req_url = '/pedidos?completed=true'
        pedidos_completed, status_code_completed = get_api_gateway(req_url)

        # Retrieve pedidos completed and delayed
        req_url = '/pedidos?completed=true&delayed=true'
        pedidos_completed_delayed, status_code_completed_delayed = get_api_gateway(
            req_url)

        if status_code_completed == 200 and status_code_completed_delayed == 200:
            # Calculate average delivery
            average_delivery = timedelta(days=0)
            for pedido in pedidos_completed:
                delivery_time = parser.parse(
                    pedido["data_entrega"]) - parser.parse(pedido["data_criacao"])
                average_delivery += delivery_time
            average_delivery /= len(pedidos_completed)

            # Calculate average delayed
            average_delayed = timedelta(days=0)
            for pedido in pedidos_completed_delayed:
                delayed_time = parser.parse(
                    pedido["data_entrega"]) - parser.parse(pedido["prazo_entrega"])
                average_delayed += delayed_time
            average_delayed /= len(pedidos_completed_delayed)

            res = {
                'completed': {
                    'total': len(pedidos_completed),
                    'average_delivery_days': round(average_delivery.total_seconds() / 86400.0, 2)
                },
                'completed_delayed': {
                    'total': len(pedidos_completed_delayed),
                    'average_delayed_days': round(average_delayed.total_seconds() / 86400.0, 2)
                }
            }
            return make_response(jsonify(res), status_code_completed)
        else:
            return make_response(jsonify({'message': 'Failed to retrieve pedidos data'}), 404)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
