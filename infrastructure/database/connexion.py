import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set in the .env file")

db_url = DATABASE_URL


def get_engine():
    return create_engine(db_url)


def get_session():
    engine = get_engine()
    Session = sessionmaker(engine)
    return Session()
