from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/postgres"

target_schema = 'public'

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False,
                       execution_options={"schema_translate_map": {None: target_schema}})

db = engine.connect()

Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)

session = Session()

Base = declarative_base()


def close_session():
    try:
        session.close()
        db.close()
        engine.dispose()
    except Exception as e:
        session.rollback()
        print("Error in closing database:", str(e))
