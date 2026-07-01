from fastapi import FastAPI
from sqlalchemy.orm import Session

from database import Base, engine, SessionLocal
import models

# Cria todas as tabelas do banco
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API UniCarona",
    description="Sistema de gerenciamento de caronas",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "mensagem": "Bem-vindo à API UniCarona!"
    }


@app.get("/teste-banco")
def teste_banco():
    db: Session = SessionLocal()

    try:
        db.execute("SELECT 1")
        return {
            "status": "Conectado ao PostgreSQL!"
        }

    finally:
        db.close()


@app.get("/usuarios")
def listar_usuarios():
    db = SessionLocal()

    try:
        usuarios = db.query(models.Usuario).all()
        return usuarios

    finally:
        db.close()


@app.get("/motoristas")
def listar_motoristas():
    db = SessionLocal()

    try:
        return db.query(models.Motorista).all()

    finally:
        db.close()


@app.get("/veiculos")
def listar_veiculos():
    db = SessionLocal()

    try:
        return db.query(models.Veiculo).all()

    finally:
        db.close()


@app.get("/locais")
def listar_locais():
    db = SessionLocal()

    try:
        return db.query(models.Local).all()

    finally:
        db.close()



@app.get("/caronas")
def listar_caronas():
    db = SessionLocal()

    try:
        return db.query(models.Carona).all()

    finally:
        db.close()


@app.get("/reservas")
def listar_reservas():
    db = SessionLocal()

    try:
        return db.query(models.Reserva).all()

    finally:
        db.close()


@app.get("/mensagens")
def listar_mensagens():
    db = SessionLocal()

    try:
        return db.query(models.Mensagem).all()

    finally:
        db.close()

@app.get("/avaliacoes")
def listar_avaliacoes():
    db = SessionLocal()

    try:
        return db.query(models.Avaliacao).all()

    finally:
        db.close()


@app.get("/pagamentos")
def listar_pagamentos():
    db = SessionLocal()

    try:
        return db.query(models.Pagamento).all()

    finally:
        db.close()