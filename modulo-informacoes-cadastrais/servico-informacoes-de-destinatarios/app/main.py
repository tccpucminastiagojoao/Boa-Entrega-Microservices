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

    from models import Destinatario
    with app.app_context():
        # Populate Destinatario with examples
        if Destinatario.query.count() == 0:
            db.session.add(Destinatario('Jorge Amado', 'Rua Via Central', 'Taubaté',
                           'São Paulo', 'Sudeste', 'Brasil', '11921124', '09319276099', ''))
            db.session.add(Destinatario('Margarida Soares', 'Avenida dos Expedicionários', 'Vargem Grande',
                           'São Paulo', 'Sudeste', 'Brasil', '11127321', '97479020015', ''))
            db.session.add(Destinatario('Simone Vieira', 'Travessa Borges de Medeiros', 'Caxias',
                           'Rio Grande do Sul', 'Sul', 'Brasil', '90123281', '76918297015', ''))
            db.session.add(Destinatario('Indústria de Móveis Horizonte', 'Rodovia Municipal CP01', 'Campo Grande',
                           'Mato Grosso do Sul', 'Centro-Oeste', 'Brasil', '79721744', '', '13555916000150'))
            db.session.add(Destinatario('Laticínios Casa da Ovelha', 'Avenida Getúlio Vargas', 'Belém',
                           'Pará', 'Norte', 'Brasil', '68984435', '', '84174647000120'))
            db.session.commit()

    @app.route('/destinatarios', methods=['GET'])
    def destinatarios():
        destinatarios = db.session.query(Destinatario).all()
        return make_response(jsonify(destinatarios), 200)

    @app.route('/destinatarios/<int:destinatario_id>', methods=['GET'])
    def get_destinatario(destinatario_id):
        destinatario = db.session.query(Destinatario).get(destinatario_id)
        if destinatario:
            return make_response(jsonify(destinatario), 200)
        else:
            return make_response(jsonify({'message': 'Destinatario Not Found'}), 404)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
