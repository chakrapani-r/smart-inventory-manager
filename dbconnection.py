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

DATABASE_URL= f"postgresql://{username}:%s@{host}:{port}/{db}" % quote_plus(password)
# print(DATABASE_URL_1)
# #DATABASE_URL_1 = DATABASE_URL_1 % quote_plus(password)
# print(DATABASE_URL_1)
# DATABASE_URL = "postgresql://postgres:%s@localhost:5432/inventory-manager" % quote_plus("Exercise@2022")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
