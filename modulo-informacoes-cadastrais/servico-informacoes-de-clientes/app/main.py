from flask import Flask, jsonify, make_response, request
import os
import sys
import requests
import numbers
import string
import random


# Postgres configuration
POSTGRES_DB = os.environ['POSTGRES_DB']
POSTGRES_USER = os.environ['POSTGRES_USER']
POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD']
POSTGRES_SERVICE = os.environ['POSTGRES_SERVICE']


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

    from models import Cliente
    with app.app_context():
        # Populate Clientes with examples
        if Cliente.query.count() == 0:
            from cadastros_exemplo import get_cadastros
            for cad in get_cadastros():
                db.session.add(Cliente(cad['nome'], cad['logradouro'], cad['cidade'],
                               cad['estado'], cad['regiao'], 'Brasil', cad['cep'], cad['cpf'], cad['cnpj']))
            db.session.commit()

    @app.route('/clientes', methods=['GET'])
    def clientes():
        clientes = db.session.query(Cliente).all()
        return make_response(jsonify(clientes), 200)

    @app.route('/clientes/<int:cliente_id>', methods=['GET'])
    def get_cliente(cliente_id):
        cliente = db.session.query(Cliente).get(cliente_id)
        if cliente:
            return make_response(jsonify(cliente), 200)
        else:
            return make_response(jsonify({'message': 'Client Not Found'}), 404)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
