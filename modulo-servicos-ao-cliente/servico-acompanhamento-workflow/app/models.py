from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
from datetime import datetime

db = SQLAlchemy()


@dataclass
class Pedido(db.Model):
    """
    Pedido
    """
    id: int
    id_cliente: int
    id_destinatario: int
    id_workflow: int
    cod_rastreio: str
    prazo_pedido: int
    valor_pedido: float
    data_criacao: datetime
    data_recebido: datetime
    data_despacho: datetime
    data_entrega: datetime

    __tablename__ = 'pedidos'

    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    id_cliente = db.Column(db.Integer)
    id_destinatario = db.Column(db.Integer)
    id_workflow = db.Column(db.Integer)
    cod_rastreio = db.Column(db.String(64))
    prazo_pedido = db.Column(db.Integer)
    valor_pedido = db.Column(db.Float)
    data_criacao = db.Column(db.DateTime)
    data_recebido = db.Column(db.DateTime)
    data_despacho = db.Column(db.DateTime)
    data_entrega = db.Column(db.DateTime)

    def __init__(self, id_cliente, id_destinatario, id_workflow, cod_rastreio, prazo_pedido, valor_pedido, data_criacao, data_recebido, data_despacho, data_entrega):
        self.id_cliente = id_cliente
        self.id_destinatario = id_destinatario
        self.id_workflow = id_workflow
        self.cod_rastreio = cod_rastreio
        self.prazo_pedido = prazo_pedido
        self.valor_pedido = valor_pedido
        self.data_criacao = data_criacao
        self.data_recebido = data_recebido
        self.data_despacho = data_despacho
        self.data_entrega = data_entrega

