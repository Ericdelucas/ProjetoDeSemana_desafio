from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import settings

Base = declarative_base()

def _build_db_url() -> str:
    # mysql+pymysql://user:password@host:port/dbname
    return (
        f"mysql+pymysql://{settings.db_user}:{settings.db_password}"
        f"@{settings.db_host}:{settings.db_port}/{settings.db_name}"
        f"?charset=utf8mb4"
    )

engine = create_engine(
    _build_db_url(),
    pool_pre_ping=True,
    pool_recycle=1800,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db() -> None:
    # Importa models para registrar no metadata antes do create_all
    from app.models.unidade import Unidade  # noqa: F401
    from app.models.estoque import Estoque  # noqa: F401
    from app.models.logs_triagem import LogTriagem  # noqa: F401

    Base.metadata.create_all(bind=engine)