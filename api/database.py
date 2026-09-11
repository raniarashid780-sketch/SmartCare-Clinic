import psycopg2
from psycopg2 import OperationalError
from dotenv import load_dotenv
import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from fastapi import FastAPI, Depends
app = FastAPI()

load_dotenv(Path(__file__).with_name(".env"))

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST", "localhost")
db_port = os.getenv("DB_PORT", "5432")
db_name = os.getenv("DB_NAME")

engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}", echo=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        return conn
    except OperationalError as e:
        print(f"[DB ERROR] Connection failed: {e}")
        return None

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()