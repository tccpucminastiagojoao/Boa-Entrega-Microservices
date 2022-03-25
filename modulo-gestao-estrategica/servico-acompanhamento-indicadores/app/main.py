from flask import Flask, jsonify, make_response, request
import os
import sys
import requests
import numbers
import string
import random
from datetime import datetime, timedelta, timezone
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
        print('API Gateway request GET:',
              api_gateway_req_url, 'Parameters:', req_params)
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
    '''
    Application factory
    '''
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

    @app.route('/indicadores', methods=['GET'])
    def indicadores():
        return make_response(jsonify({'message': 'indicadores'}), 200)

    @app.route('/indicadores/pedidos', methods=['GET'])
    def get_indicadores_pedidos():
        """
        Get indicadores pedidos
        US3 : Acompanhamento das metas estratégicas
        """
        # Datetime now
        datetime_now = datetime.now(timezone.utc)

        def retrieve_pedidos(base_req_url):
            """
            Retrieve pedidos with pagination
            """
            page = 0
            pedidos_res = []
            status_code_res = 200

            while(True):
                req_url = '{0}&page={1}&pageSize=200'.format(
                    base_req_url, page)
                pedidos, status_code = get_api_gateway(req_url)
                if status_code == 200:
                    if len(pedidos) > 0:
                        pedidos_res.extend(pedidos)
                        page += 1
                    else:
                        break
                else:
                    status_code_res = status_code
                    break

            return pedidos_res, status_code_res

        # Retrieve pedidos completed
        req_url = '/pedidos?completed=true'
        pedidos_completed, status_code_completed = \
            retrieve_pedidos(req_url)

        # Retrieve pedidos completed and delayed
        req_url = '/pedidos?completed=true&delayed=true'
        pedidos_completed_delayed, status_code_completed_delayed = \
            retrieve_pedidos(req_url)

        # Retrieve pedidos active
        req_url = '/pedidos?active=true'
        pedidos_active, status_code_active = \
            retrieve_pedidos(req_url)

        # Retrieve pedidos active and delayed
        req_url = '/pedidos?active=true&delayed=true'
        pedidos_active_delayed, status_code_active_delayed = \
            retrieve_pedidos(req_url)

        if status_code_completed == 200 and status_code_completed_delayed == 200 \
                and status_code_active == 200 and status_code_active_delayed == 200:
            # Cities
            cliente_ids = []
            destinatarios_ids = []
            clientes_cities = []
            destinatarios_cities = []

            # Calculate revenues completed, average delivery completed
            revenues_completed = 0.0
            average_delivery_completed = timedelta(days=0)

            for pedido in pedidos_completed:
                revenues_completed += float(pedido['valor_pedido'])
                delivery_time = parser.parse(pedido['data_entrega']) - \
                    parser.parse(pedido['data_criacao'])
                average_delivery_completed += delivery_time

                # Store id_cliente and id_destinatario
                id_cliente = pedido['id_cliente']
                if id_cliente not in cliente_ids:
                    cliente_ids.append(id_cliente)
                id_destinatario = pedido['id_destinatario']
                if id_destinatario not in destinatarios_ids:
                    destinatarios_ids.append(id_destinatario)

            try:
                average_delivery_completed /= len(pedidos_completed)
            except ZeroDivisionError:
                average_delivery_completed = timedelta(days=0)

            # Calculate average delayed completed
            average_delayed_completed = timedelta(days=0)
            for pedido in pedidos_completed_delayed:
                delayed_time = parser.parse(pedido['data_entrega']) - \
                    parser.parse(pedido['prazo_entrega'])
                average_delayed_completed += delayed_time

            try:
                average_delayed_completed /= len(pedidos_completed_delayed)
            except ZeroDivisionError:
                average_delayed_completed = timedelta(days=0)

            # Calculate revenues active, average delivery active
            revenues_active = 0.0
            average_in_delivery_active = timedelta(days=0)
            for pedido in pedidos_active:
                revenues_active += float(pedido['valor_pedido'])
                delivery_time = datetime_now - \
                    parser.parse(pedido['data_criacao'])
                average_in_delivery_active += delivery_time

                # Store id_cliente and id_destinatario
                id_cliente = pedido['id_cliente']
                if id_cliente not in cliente_ids:
                    cliente_ids.append(id_cliente)
                id_destinatario = pedido['id_destinatario']
                if id_destinatario not in destinatarios_ids:
                    destinatarios_ids.append(id_destinatario)

            try:
                average_in_delivery_active /= len(pedidos_active)
            except ZeroDivisionError:
                average_in_delivery_active = timedelta(days=0)

            # Calculate average delayed active
            average_in_delayed_active = timedelta(days=0)
            for pedido in pedidos_active_delayed:
                delivery_time = datetime_now - \
                    parser.parse(pedido['data_criacao'])
                average_in_delayed_active += delayed_time

            try:
                average_in_delayed_active /= len(pedidos_active_delayed)
            except ZeroDivisionError:
                average_in_delayed_active = timedelta(days=0)

            for id_cliente in cliente_ids:
                req_url = '/clientes/{0}'.format(id_cliente)
                cliente, status_code_cliente = get_api_gateway(req_url)
                if status_code_cliente == 200:
                    cidade = cliente['cidade']
                    if cidade not in clientes_cities:
                        clientes_cities.append(cidade)

            for id_destinatario in destinatarios_ids:
                req_url = '/destinatarios/{0}'.format(id_destinatario)
                destinatario, status_code_destinatario = get_api_gateway(req_url)
                if status_code_destinatario == 200:
                    cidade = destinatario['cidade']
                    if cidade not in destinatarios_cities:
                        destinatarios_cities.append(cidade)

            res = {
                'completed': {
                    'total': len(pedidos_completed),
                    'revenues': round(revenues_completed, 2),
                    'average_delivery_days': round(average_delivery_completed.total_seconds() / 86400.0, 2)
                },
                'completed_delayed': {
                    'total': len(pedidos_completed_delayed),
                    'average_delayed_days': round(average_delayed_completed.total_seconds() / 86400.0, 2)
                },
                'active': {
                    'total': len(pedidos_active),
                    'revenues': round(revenues_active, 2),
                    'average_in_delivery_days': round(average_in_delivery_active.total_seconds() / 86400.0, 2)
                },
                'active_delayed': {
                    'total': len(pedidos_active_delayed),
                    'average_in_delayed_days': round(average_in_delayed_active.total_seconds() / 86400.0, 2)
                },
                'cities_attended': {
                    'clientes': len(clientes_cities),
                    'destinatarios': len(destinatarios_cities)
                }
            }
            return make_response(jsonify(res), status_code_completed)
        else:
            return make_response(jsonify({'message': 'Failed to retrieve pedidos data'}), 404)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
