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
            db.session.add(Cliente('José Silva', 'Rua das Camélias', 'Riberão Preto',
                           'São Paulo', 'Sudeste', 'Brasil', '11324-333', '123.456.789-99', ''))
            db.session.add(Cliente('Maria Pereira', 'Rua dos Navegantes', 'Riberão Preto',
                           'São Paulo', 'Sudeste', 'Brasil', '11324-127', '123.456.789-99', ''))
            db.session.add(Cliente('Guilherme Tell', 'Rua Brasília', 'Porto Alegre',
                           'Rio Grande do Sul', 'Sul', 'Brasil', '90010-437', '123.456.789-99', ''))
            db.session.add(Cliente('Confecções Amor de Bicho', 'Estrada Geral Rinção das Alegrias', 'Dourados',
                           'Mato Grosso do Sul', 'Centro-Oeste', 'Brasil', '79800-701', '', '12.345.678/0001-99'))
            db.session.add(Cliente('Marcenaria Pau Brasil', 'Rodovia Via Expressa 734', 'Santarém',
                           'Pará', 'Norte', 'Brasil', '68000-251', '', '12.345.678/0001-99'))
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
