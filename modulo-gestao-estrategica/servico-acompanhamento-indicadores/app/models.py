from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
from datetime import datetime, timedelta


db = SQLAlchemy()


@dataclass
class Indicador(db.Model):
    """
    Indicador
    """
    id: int
    nome: str
    data_criacao: datetime

    __tablename__ = 'indicadores'

    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    nome = db.Column(db.String(128))
    data_criacao = db.Column(db.DateTime)

    def __init__(self, nome, data_criacao):
        self.nome = nome
        self.data_criacao = data_criacao
