from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url = 'sqlite:///infrastructure/database/fiche_contact.db'

def get_engine():
       return create_engine(db_url)

def get_session():
       engine = get_engine()
       Session = sessionmaker(engine)
       return Session()