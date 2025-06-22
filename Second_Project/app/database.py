from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import setting

SQLALCHEMY_DATABASE_URL = f"postgresql://{setting.database_username}:{setting.database_password}@{setting.database_hostname}:{setting.database_port}/{setting.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# # connecting the database to our project
# while True:
#     try:
#         conn = psycopg2.connect(host='your domain/localhost',   database='database_name', user='user_name',  password='enter password', cursor_factory=RealDictCursor)

#         cursor = conn.cursor()
#         print("🛢️  Database connection successfull: Postgres")
#         break
#     except Exception as error:
#         print(f"Error connecting to database: {error}")
#         time.sleep(2)

