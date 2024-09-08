import time
import psycopg2
from sqlalchemy import create_engine

from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine( SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def psycopConnect():
    while True:
        try:
            conn = psycopg2.connect(host = settings.database_hostname, database = settings.database_name, 
                            user = settings.database_username, password = settings.database_password, 
                            port =settings.database_port, cursor_factory=RealDictCursor)
            
            cursor = conn.cursor()

            print("DB connection success")
            break
        
        except Exception as error:
            print("DB connection error", error)
            time.sleep(2)

    return conn, cursor