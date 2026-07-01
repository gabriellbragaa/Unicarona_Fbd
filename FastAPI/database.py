from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# Altere para os dados do seu PostgreSQL
DATABASE_URL = "postgresql://postgres:senha@localhost:5432/unicarona"

# Cria a conexão com o banco
engine = create_engine(
    DATABASE_URL,
    echo=True
)

# Cria uma sessão para cada requisição
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Classe base para os modelos
Base = declarative_base()


# Dependência utilizada pelo FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()