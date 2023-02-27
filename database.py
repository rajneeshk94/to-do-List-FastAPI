from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_URL = "mysql://root:@localhost/to-doList"

engine = create_engine(DB_URL)

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, bind=engine)
