import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

load_dotenv()


def source_engine() -> Engine:
    host = os.environ["SOURCE_DB_HOST"]
    port = os.environ["SOURCE_DB_PORT"]
    name = os.environ["SOURCE_DB_NAME"]
    user = os.environ["SOURCE_DB_USER"]
    password = os.environ["SOURCE_DB_PASSWORD"]
    url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}"
    return create_engine(url)
