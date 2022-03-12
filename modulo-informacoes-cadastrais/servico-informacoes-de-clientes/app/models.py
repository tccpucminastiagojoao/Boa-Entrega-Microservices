from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass


db = SQLAlchemy()


@dataclass
class Cliente(db.Model):
    """
    Cliente
    """
    id: int
    nome: str
    logradouro: str
    cidade: str
    estado: str
    regiao: str
    pais: str
    cep: str
    cpf: str
    cnpj: str

    __tablename__ = 'clientes'

    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    nome = db.Column(db.String(128))
    logradouro = db.Column(db.String(64))
    cidade = db.Column(db.String(64))
    estado = db.Column(db.String(64))
    regiao = db.Column(db.String(64))
    pais = db.Column(db.String(64))
    cep = db.Column(db.String(64))
    cpf = db.Column(db.String(64))
    cnpj = db.Column(db.String(64))

    def __init__(self, nome, logradouro, cidade, estado, regiao, pais, cep, cpf, cnpj):
        self.nome = nome
        self.logradouro = logradouro
        self.cidade = cidade
        self.estado = estado
        self.regiao = regiao
        self.pais = pais
        self.cep = cep
        self.cpf = cpf
        self.cnpj = cnpj


@dataclass
class Destinatario(db.Model):
    """
    Destinatario
    """
    id: int
    nome: str
    logradouro: str
    cidade: str
    estado: str
    regiao: str
    pais: str
    cep: str
    cpf: str
    cnpj: str

    __tablename__ = 'destinatarios'

    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    nome = db.Column(db.String(128))
    logradouro = db.Column(db.String(64))
    cidade = db.Column(db.String(64))
    estado = db.Column(db.String(64))
    regiao = db.Column(db.String(64))
    pais = db.Column(db.String(64))
    cep = db.Column(db.String(64))
    cpf = db.Column(db.String(64))
    cnpj = db.Column(db.String(64))

    def __init__(self, nome, logradouro, cidade, estado, regiao, pais, cep, cpf, cnpj):
        self.nome = nome
        self.logradouro = logradouro
        self.cidade = cidade
        self.estado = estado
        self.regiao = regiao
        self.pais = pais
        self.cep = cep
        self.cpf = cpf
        self.cnpj = cnpj
