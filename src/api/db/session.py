import sqlmodel
from sqlmodel import SQLModel, Session
from .config import DATABASE_URL, DB_TIMEZONE
import timescaledb

if DATABASE_URL == "":
    raise NotImplemetedError("DATABASE_URL needs to be set")
# engine = ??
engine = timescaledb.create_engine(DATABASE_URL, timezone=DB_TIMEZONE)


def init_db():
    print("Creating Database")
    SQLModel.metadata.create_all(engine)
    print("Creating TimescaleDB Hypertable")
    timescaledb.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
