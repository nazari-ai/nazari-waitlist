from sqlalchemy import create_engine
from typing import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

#SQLALCHEMY_DATABASE_URL = "sqlite:///./waitlist.db"
SQLALCHEMY_DATABASE_URL= "postgres://uovyxjmplmasat:1288339d5826bd87fc58414d15d03ada76d0247c96bf34234e2f18fb4e87e51e@ec2-34-235-31-124.compute-1.amazonaws.com:5432/dgsokp4o8nq2v"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()

