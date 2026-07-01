from sqlalchemy import Column, String, Integer, Date, Time, Text, Numeric, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Usuario(Base):
    __tablename__ = "usuario"

    cpf = Column(String(11), primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    telefone = Column(String(15))

    motorista = relationship("Motorista", back_populates="usuario", uselist=False)

    reservas = relationship("Reserva", back_populates="usuario")

    mensagens_enviadas = relationship(
        "Mensagem",
        foreign_keys="Mensagem.cpf_remetente",
        back_populates="remetente"
    )

    mensagens_recebidas = relationship(
        "Mensagem",
        foreign_keys="Mensagem.cpf_destinatario",
        back_populates="destinatario"
    )

    avaliacoes_feitas = relationship(
        "Avaliacao",
        foreign_keys="Avaliacao.cpf_avaliador",
        back_populates="avaliador"
    )

    avaliacoes_recebidas = relationship(
        "Avaliacao",
        foreign_keys="Avaliacao.cpf_avaliado",
        back_populates="avaliado"
    )

class Motorista(Base):
    __tablename__ = "motorista"

    cpf = Column(String(11), ForeignKey("usuario.cpf"), primary_key=True)
    numero_cnh = Column(String(20), unique=True, nullable=False)
    validade_cnh = Column(Date, nullable=False)

    usuario = relationship("Usuario", back_populates="motorista")

    veiculos = relationship("Veiculo", back_populates="motorista")

    caronas = relationship("Carona", back_populates="motorista")

class Veiculo(Base):
    __tablename__ = "veiculo"

    placa = Column(String(7), primary_key=True)
    cpf_motorista = Column(String(11), ForeignKey("motorista.cpf"))

    modelo = Column(String(50), nullable=False)
    marca = Column(String(50), nullable=False)
    cor = Column(String(30))
    capacidade_passageiros = Column(Integer, nullable=False)

    motorista = relationship("Motorista", back_populates="veiculos")

    caronas = relationship("Carona", back_populates="veiculo")

class Local(Base):
    __tablename__ = "local"

    id_local = Column(Integer, primary_key=True)

    nome_local = Column(String(100), nullable=False)
    cidade = Column(String(50), nullable=False)
    bairro = Column(String(50))

    origem = relationship(
        "Carona",
        foreign_keys="Carona.id_origem",
        back_populates="local_origem"
    )

    destino = relationship(
        "Carona",
        foreign_keys="Carona.id_destino",
        back_populates="local_destino"
    )

class Carona(Base):
    __tablename__ = "carona"

    id_carona = Column(Integer, primary_key=True)

    cpf_motorista = Column(
        String(11),
        ForeignKey("motorista.cpf"),
        nullable=False
    )

    placa_veiculo = Column(
        String(7),
        ForeignKey("veiculo.placa"),
        nullable=False
    )

    id_origem = Column(
        Integer,
        ForeignKey("local.id_local"),
        nullable=False
    )

    id_destino = Column(
        Integer,
        ForeignKey("local.id_local"),
        nullable=False
    )

    data = Column(Date, nullable=False)
    horario = Column(Time, nullable=False)

    vagas_disponiveis = Column(Integer, nullable=False)

    motorista = relationship("Motorista", back_populates="caronas")

    veiculo = relationship("Veiculo", back_populates="caronas")

    local_origem = relationship(
        "Local",
        foreign_keys=[id_origem],
        back_populates="origem"
    )

    local_destino = relationship(
        "Local",
        foreign_keys=[id_destino],
        back_populates="destino"
    )

    reservas = relationship("Reserva", back_populates="carona")


class Reserva(Base):
    __tablename__ = "reserva"

    id_reserva = Column(Integer, primary_key=True)

    cpf_usuario = Column(
        String(11),
        ForeignKey("usuario.cpf"),
        nullable=False
    )

    id_carona = Column(
        Integer,
        ForeignKey("carona.id_carona"),
        nullable=False
    )

    status = Column(String(20), nullable=False)

    data_reserva = Column(Date, nullable=False)

    usuario = relationship("Usuario", back_populates="reservas")

    carona = relationship("Carona", back_populates="reservas")

    pagamento = relationship(
        "Pagamento",
        back_populates="reserva",
        uselist=False
    )

class Mensagem(Base):
    __tablename__ = "mensagem"

    id_mensagem = Column(Integer, primary_key=True)

    cpf_remetente = Column(
        String(11),
        ForeignKey("usuario.cpf"),
        nullable=False
    )

    cpf_destinatario = Column(
        String(11),
        ForeignKey("usuario.cpf"),
        nullable=False
    )

    conteudo = Column(Text, nullable=False)

    data_envio = Column(Date, nullable=False)

    remetente = relationship(
        "Usuario",
        foreign_keys=[cpf_remetente],
        back_populates="mensagens_enviadas"
    )

    destinatario = relationship(
        "Usuario",
        foreign_keys=[cpf_destinatario],
        back_populates="mensagens_recebidas"
    )

class Avaliacao(Base):
    __tablename__ = "avaliacao"

    id_avaliacao = Column(Integer, primary_key=True)

    cpf_avaliador = Column(
        String(11),
        ForeignKey("usuario.cpf"),
        nullable=False
    )

    cpf_avaliado = Column(
        String(11),
        ForeignKey("usuario.cpf"),
        nullable=False
    )

    nota = Column(Integer, nullable=False)

    comentario = Column(Text)

    data = Column(Date, nullable=False)

    avaliador = relationship(
        "Usuario",
        foreign_keys=[cpf_avaliador],
        back_populates="avaliacoes_feitas"
    )

    avaliado = relationship(
        "Usuario",
        foreign_keys=[cpf_avaliado],
        back_populates="avaliacoes_recebidas"
    )

class Pagamento(Base):
    __tablename__ = "pagamento"

    id_pagamento = Column(Integer, primary_key=True)

    id_reserva = Column(
        Integer,
        ForeignKey("reserva.id_reserva"),
        nullable=False
    )

    valor = Column(Numeric(10, 2), nullable=False)

    status = Column(String(20), nullable=False)

    forma_pagamento = Column(String(30), nullable=False)

    data_pagamento = Column(Date)

    reserva = relationship(
        "Reserva",
        back_populates="pagamento"
    )