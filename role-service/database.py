from sqlmodel import create_engine, Session, SQLModel, select
from sqlalchemy.engine import Engine
from enums.role import RoleEnum
from settings import get_settings
from tables.role import Role

ROLES = [RoleEnum.ADMIN, RoleEnum.USER]


def create_db_engine(settings) -> Engine:
    db_root_user = settings.MYSQL_USER
    db_root_password = settings.MYSQL_PASSWORD
    db_host = settings.DB_HOST
    db_port = settings.DB_PORT
    db_name = settings.MYSQL_DATABASE
    DATABASE_URL = f"mysql+pymysql://{db_root_user}:{db_root_password}@{db_host}:{db_port}/{db_name}"

    return create_engine(DATABASE_URL)

engine = create_db_engine(get_settings())

def create_default_roles(session: Session):
    for role in ROLES:
        statement = select(Role).where(Role.role == role)
        existingRole = session.exec(statement).first()

        if not existingRole:
            rollToInject = Role(role=role)
            session.add(rollToInject)

    session.commit()


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        create_default_roles(session)


def get_session():
    with Session(engine) as session:
        yield session

    
