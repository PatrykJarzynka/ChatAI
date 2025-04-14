from sqlmodel import create_engine, Session, SQLModel
from sqlalchemy.engine import Engine
from config import get_settings

def create_db_engine(settings) -> Engine:
    db_root_user = settings.MYSQL_USER
    db_root_password = settings.MYSQL_PASSWORD
    db_host = settings.DB_HOST
    db_port = settings.DB_PORT
    db_name = settings.MYSQL_DATABASE
    DATABASE_URL = f"mysql+pymysql://{db_root_user}:{db_root_password}@{db_host}:{db_port}/{db_name}"

    return create_engine(DATABASE_URL)

engine = create_db_engine(get_settings())

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

    
