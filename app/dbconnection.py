from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from decouple import config
# Needed to handle special chars in password
from urllib.parse import quote_plus

username = JWT_SECRET = config("db_user")
password = config("db_password")
host = config("db_host")
db = config("db_name")
port = config("db_port")
print(password)
DATABASE_URL= f"postgresql://{username}:%s@{host}:{port}/{db}" % quote_plus(password)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
