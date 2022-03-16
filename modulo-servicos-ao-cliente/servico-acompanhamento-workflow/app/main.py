from flask import Flask, jsonify, make_response, request
import os
import sys
import requests
import numbers
import string
import random
import json
from datetime import datetime, timedelta

from sqlalchemy import false

# Postgres configuration
POSTGRES_DB = os.environ['POSTGRES_DB']
POSTGRES_USER = os.environ['POSTGRES_USER']
POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD']
POSTGRES_SERVICE = os.environ['POSTGRES_SERVICE']

# Jbpm configuration
JBPM_SERVICE = os.environ['JBPM_SERVICE']

JBPM_API_URL = 'http://{0}:8080/kie-server/services/rest'.format(JBPM_SERVICE)
JBPM_JSON_HEADERS = {'accept': 'application/json',
                     'content-type': 'application/json'}
JBPM_SVG_HEADERS = {'accept': 'application/svg+xml',
                    'content-type': 'application/svg+xml'}
JBPM_AUTH = ('wbadmin', 'wbadmin')
JBPM_CONTAINER_ID = 'Boa-Entrega_1.0.0-SNAPSHOT'
JBPM_PROCESS_ID = 'Boa-Entrega.Entrega-Padrao'


def get_jbpm_server(req_url, req_params={}):
    try:
        jbpm_req_url = '{0}{1}'.format(JBPM_API_URL, req_url)
        print("jBPM request GET:", jbpm_req_url, "Parameters:", req_params)
        req_res = requests.get(
            url=jbpm_req_url, headers=JBPM_JSON_HEADERS, auth=JBPM_AUTH, params=req_params)
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
            JBPM_API_URL, req_url)
        return req_res_error, 503


def get_svg_jbpm_server(req_url, req_params={}):
    try:
        jbpm_req_url = '{0}{1}'.format(JBPM_API_URL, req_url)
        print("jBPM request GET:", jbpm_req_url, "Parameters:", req_params)
        req_res = requests.get(
            url=jbpm_req_url, headers=JBPM_SVG_HEADERS, auth=JBPM_AUTH, params=req_params)

        if req_res.status_code == 200:
            req_res_decoded = req_res.content.decode('utf-8')
            return req_res_decoded, req_res.status_code
        else:
            req_res_text = req_res.text
            return req_res_text, req_res.status_code
    except requests.exceptions.ConnectionError:
        req_res_error = 'Failed to establish a connection: {0}{1}'.format(
            JBPM_API_URL, req_url)
        return req_res_error, 503


def post_jbpm_server(req_url, req_data={}):
    try:
        jbpm_req_url = '{0}{1}'.format(JBPM_API_URL, req_url)
        print("jBPM request POST:", jbpm_req_url, "Data:", req_data)
        req_res = requests.post(
            url=jbpm_req_url, headers=JBPM_JSON_HEADERS, auth=JBPM_AUTH, data=req_data)
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
            JBPM_API_URL, req_url)
        return req_res_error, 503


def put_jbpm_server(req_url, req_data={}):
    try:
        jbpm_req_url = '{0}{1}'.format(JBPM_API_URL, req_url)
        print("jBPM request PUT:", jbpm_req_url, "Data:", req_data)
        req_res = requests.put(
            url=jbpm_req_url, headers=JBPM_JSON_HEADERS, auth=JBPM_AUTH, data=req_data)
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
            JBPM_API_URL, req_url)
        return req_res_error, 503


def get_nodes_by_type(data, type):
    return [node for node in data['node-instance'] if node['node-type'] == type]


def get_nodes_by_name(data, name):
    return [node for node in data['node-instance'] if node['node-name'] == name]


def get_random_cod_rastreio():
    letters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(letters) for i in range(32))


def get_pedido_data(pedido):
    data = jsonify(pedido).get_json()
    data['links'] = {
        'self': '{0}pedidos/{1}'.format(request.url_root, pedido.id),
        'nodes': '{0}pedidos/{1}/nodes'.format(request.url_root, pedido.id),
        'node-by-type': '{0}pedidos/{1}/nodes/type/node_type'.format(request.url_root, pedido.id),
        'node-by-name': '{0}pedidos/{1}/nodes/name/node_name'.format(request.url_root, pedido.id),
        'workitems': '{0}pedidos/{1}/workitems'.format(request.url_root, pedido.id),
        'complete-workitem': '{0}pedidos/{1}/workitems/workitem_index/complete'.format(request.url_root, pedido.id),
        'images': '{0}pedidos/{1}/images'.format(request.url_root, pedido.id)
    }
    return data


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
        # db.drop_all()  # Only for tests with data examples
        db.create_all()
        db.session.commit()

    from models import Pedido
    # with app.app_context():
    # Populate Pedidos with examples
    # if Pedido.query.count() == 0:
    #     db.session.add(Pedido(4, 2, 1, "AAABBBCCC", 1.5, 19.57,
    #                    datetime.now(), datetime.now() + timedelta(days=2)))
    #     db.session.add(Pedido(3, 5, 1, "ZZZMMMJJJ", 4.5, 33.25,
    #                    datetime.now(), datetime.now() + timedelta(days=3)))
    #     db.session.commit()

    @app.route('/pedidos', methods=['GET'])
    def pedidos():
        '''
        Get all pedidos
        '''
        page = int(request.args.get('page', '0'))
        pageSize = int(request.args.get('pageSize', '999'))

        if request.args.get('completed', 'false') == 'true':
            pedidos = [get_pedido_data(pedido) for pedido in db.session.query(
                Pedido).filter(Pedido.data_entrega != None).limit(pageSize).offset(page*pageSize)]
        elif request.args.get('active', 'false') == 'true':
            pedidos = [get_pedido_data(pedido) for pedido in db.session.query(
                Pedido).filter(Pedido.data_entrega == None).limit(pageSize).offset(page*pageSize)]
        else:
            pedidos = [get_pedido_data(pedido) for pedido in db.session.query(
                Pedido).limit(pageSize).offset(page*pageSize).all()]

        return make_response(jsonify(pedidos), 200)

    # jBPM = POST /server/containers/{containerId}/processes/{processId}/instances
    @app.route('/pedidos', methods=['POST'])
    def create_pedido():
        '''
        Create new pedido
        '''
        post_id_cliente = request.form.get('id_cliente')
        post_id_destinatario = request.form.get('id_destinatario')
        if post_id_cliente and post_id_destinatario:
            req_url = '/server/containers/{0}/processes/{1}/instances'.format(
                JBPM_CONTAINER_ID, JBPM_PROCESS_ID)
            data, status_code = post_jbpm_server(req_url)

            if status_code == 201:
                # Process intace created in jBPM
                post_id_workflow = data

                # Create new codigo rastreio
                new_cod_rastreio = get_random_cod_rastreio()
                while(db.session.query(db.exists().where(
                        Pedido.cod_rastreio == new_cod_rastreio)).scalar()):
                    new_cod_rastreio = get_random_cod_rastreio()

                # Save pedido data
                pedido = Pedido(id_cliente=int(post_id_cliente),
                                id_destinatario=int(post_id_destinatario),
                                id_workflow=int(post_id_workflow),
                                cod_rastreio=new_cod_rastreio,
                                prazo_pedido=1.0,
                                valor_pedido=1.0,
                                data_despacho=None,
                                data_entrega=None)
                db.session.add(pedido)
                db.session.commit()
                data = get_pedido_data(pedido)
                return make_response(jsonify(data), 201)
            else:
                return make_response(data, status_code)
        else:
            return make_response(jsonify({'message': 'Check request form data'}), 400)

    @app.route('/pedidos/<int:pedido_id>', methods=['GET'])
    def get_pedido(pedido_id):
        '''
        Get specific pedido information
        '''
        pedido = db.session.query(Pedido).get(pedido_id)
        if pedido:
            data = get_pedido_data(pedido)
            return make_response(jsonify(data), 200)
        else:
            return make_response(jsonify({'message': 'Pedido Not Found'}), 404)

    # jBPM = GET /server/containers/{containerId}/processes/instances/{processInstanceId}/nodes/instances
    @app.route('/pedidos/<int:pedido_id>/nodes', methods=['GET'])
    def get_pedido_nodes(pedido_id):
        '''
        Get specific pedido workflow nodes
        '''
        pedido = db.session.query(Pedido).get(pedido_id)
        if pedido:
            req_params = {'page': request.args.get('page', '0'),
                          'pageSize': request.args.get('pageSize', '999')}

            if request.args.get('completed', 'false') == 'true':
                req_params['completedOnly'] = 'true'
            elif request.args.get('active', 'false') == 'true':
                req_params['activeOnly'] = 'true'

            req_url = '/server/containers/{0}/processes/instances/{1}/nodes/instances'.format(
                JBPM_CONTAINER_ID, pedido.id_workflow)
            data, status_code = get_jbpm_server(req_url, req_params)
            if status_code == 200 and 'node-instance' in data:
                return make_response(jsonify(data['node-instance']), status_code)
            else:
                return make_response(data, status_code)
        else:
            return make_response(jsonify({'message': 'Pedido Not Found'}), 404)

    # jBPM = GET /server/containers/{containerId}/processes/instances/{processInstanceId}/nodes/instances
    @app.route('/pedidos/<int:pedido_id>/nodes/type/<node_type>', methods=['GET'])
    def get_pedido_nodes_by_type(pedido_id, node_type):
        '''
        Get specific pedido workflow start node
        '''
        pedido = db.session.query(Pedido).get(pedido_id)
        if pedido:
            req_params = {'page': request.args.get('page', '0'),
                          'pageSize': request.args.get('pageSize', '999')}

            if request.args.get('completed', 'false') == 'true':
                req_params['completedOnly'] = 'true'
            elif request.args.get('active', 'false') == 'true':
                req_params['activeOnly'] = 'true'

            req_url = '/server/containers/{0}/processes/instances/{1}/nodes/instances'.format(
                JBPM_CONTAINER_ID, pedido.id_workflow)
            data, status_code = get_jbpm_server(req_url, req_params)
            if status_code == 200 and 'node-instance' in data:
                nodes = get_nodes_by_type(data, node_type)
                return make_response(jsonify(nodes), 200)
            else:
                return make_response(data, status_code)
        else:
            return make_response(jsonify({'message': 'Pedido Not Found'}), 404)

    # jBPM = GET /server/containers/{containerId}/processes/instances/{processInstanceId}/nodes/instances
    @app.route('/pedidos/<int:pedido_id>/nodes/name/<node_name>', methods=['GET'])
    def get_pedido_nodes_by_name(pedido_id, node_name):
        '''
        Get specific pedido workflow start node
        '''
        pedido = db.session.query(Pedido).get(pedido_id)
        if pedido:
            req_params = {'page': request.args.get('page', '0'),
                          'pageSize': request.args.get('pageSize', '999')}

            if request.args.get('completed', 'false') == 'true':
                req_params['completedOnly'] = 'true'
            elif request.args.get('active', 'false') == 'true':
                req_params['activeOnly'] = 'true'

            req_url = '/server/containers/{0}/processes/instances/{1}/nodes/instances'.format(
                JBPM_CONTAINER_ID, pedido.id_workflow)
            data, status_code = get_jbpm_server(req_url, req_params)
            if status_code == 200 and 'node-instance' in data:
                nodes = get_nodes_by_name(data, node_name)
                return make_response(jsonify(nodes), 200)
            else:
                return make_response(data, status_code)
        else:
            return make_response(jsonify({'message': 'Pedido Not Found'}), 404)

    # jBPM = GET /server/containers/{containerId}/processes/instances/{processInstanceId}/workitems
    @app.route('/pedidos/<int:pedido_id>/workitems', methods=['GET'])
    def get_pedido_workitems(pedido_id):
        '''
        Get specific pedido workflow workitens
        '''
        pedido = db.session.query(Pedido).get(pedido_id)
        if pedido:
            req_url = '/server/containers/{0}/processes/instances/{1}/workitems'.format(
                JBPM_CONTAINER_ID, pedido.id_workflow)
            data, status_code = get_jbpm_server(req_url)
            if status_code == 200 and 'work-item-instance' in data:
                return make_response(jsonify(data['work-item-instance']), status_code)
            else:
                return make_response(data, status_code)
        else:
            return make_response(jsonify({'message': 'Pedido Not Found'}), 404)

    # jBPM = PUT /server/containers/{containerId}/processes/instances/{processInstanceId}/workitems/{workItemId}/completed
    @app.route('/pedidos/<int:pedido_id>/workitems/<int:workitem_index>/complete', methods=['PUT'])
    def complete_pedido_workitem(pedido_id, workitem_index):
        '''
        Complete specific pedido workflow workiten
        '''
        pedido = db.session.query(Pedido).get(pedido_id)
        if pedido:
            # Get workitems
            req_url = '/server/containers/{0}/processes/instances/{1}/workitems'.format(
                JBPM_CONTAINER_ID, pedido.id_workflow)
            data, status_code = get_jbpm_server(req_url)
            if status_code == 200 and 'work-item-instance' in data:
                workitems = data['work-item-instance']
                try:
                    workitem = workitems[workitem_index]
                    workitem_id = workitem['work-item-id']
                    workitem_node_name = workitem['work-item-params']['NodeName']

                    # Check events
                    if workitem_node_name == 'Envio':
                        pedido.data_despacho = datetime.now()
                        db.session.commit()
                    if workitem_node_name == 'Entregue':
                        pedido.data_entrega = datetime.now()
                        db.session.commit()

                    # Complete workitem
                    req_url = '/server/containers/{0}/processes/instances/{1}/workitems/{2}/completed'.format(
                        JBPM_CONTAINER_ID, pedido.id_workflow, workitem_id)
                    data, status_code = put_jbpm_server(req_url)
                    if status_code == 201:
                        return make_response(jsonify({'message': 'Workitem completed', 'workitem': workitem}), 201)
                    else:
                        return make_response(data, status_code)
                except IndexError:
                    return make_response(jsonify({'message': 'Workitem Not Found'}), 404)
            else:
                return make_response(jsonify({'message': 'Workitem Not Found'}), 404)
        else:
            return make_response(jsonify({'message': 'Pedido Not Found'}), 404)

    # jBPM = /server/containers/{containerId}/images/processes/instances/{processInstanceId}
    @app.route('/pedidos/<int:pedido_id>/images', methods=['GET'])
    def get_pedido_images(pedido_id):
        '''
        Get specific pedido SVG workflow image
        '''
        pedido = db.session.query(Pedido).get(pedido_id)
        if pedido:
            req_url = '/server/containers/{0}/images/processes/instances/{1}'.format(
                JBPM_CONTAINER_ID, pedido.id_workflow)
            data, status_code = get_svg_jbpm_server(req_url)
            req_res = make_response(data, status_code)
            if status_code == 200:
                req_res.content_type = 'application/xml;charset=UTF-8'
            return req_res
        else:
            return make_response(jsonify({'message': 'Pedido Not Found'}), 404)

    # jBPM = /server/containers/{containerId}/processes/definitions/{processId}
    @app.route('/pedidos/process/definitions', methods=['GET'])
    def get_process_definitions():
        '''
        Get general pedido workflow definitions
        '''
        req_url = '/server/containers/{0}/processes/definitions/{1}'.format(
            JBPM_CONTAINER_ID, JBPM_PROCESS_ID)
        data, status_code = get_jbpm_server(req_url)
        return make_response(data, status_code)

    # jBPM = /server/containers/{containerId}/images/processes/{processId}
    @app.route('/pedidos/process/images', methods=['GET'])
    def get_process_images():
        '''
        Get general pedido workflow image
        '''
        req_url = '/server/containers/{0}/images/processes/{1}'.format(
            JBPM_CONTAINER_ID, JBPM_PROCESS_ID)
        data, status_code = get_svg_jbpm_server(req_url)
        if status_code == 200:
            req_res = make_response(data, status_code)
            #req_res.mimetype = 'application/svg+xml'
            req_res.content_type = 'application/xml;charset=UTF-8'
            return req_res
        else:
            return make_response(data, status_code)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
