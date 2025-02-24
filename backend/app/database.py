import os

from dotenv import load_dotenv
from sqlmodel import create_engine, Session, SQLModel

env_file = ".env.production" if os.getenv("DOCKER_ENV") == "production" else ".env.development"

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env_path = os.path.join(base_dir, env_file)

load_dotenv(env_path)

db_root_user = os.getenv("MYSQL_USER")
db_root_password = os.getenv("MYSQL_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("MYSQL_DATABASE")


DATABASE_URL = f"mysql+pymysql://{db_root_user}:{db_root_password}@{db_host}:{db_port}/{db_name}"

engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
