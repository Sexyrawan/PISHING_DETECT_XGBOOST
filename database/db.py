from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

db_url = "sqlite:///./phshing.db"

engine = create_engine(
    db_url,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,   # don't save automatically, we control it
    autoflush=False,    # don't send to DB until we say so
    bind=engine         # use our engine/connection
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db        # ← 'yield' pauses here, gives db to route
    finally:
        db.close()  