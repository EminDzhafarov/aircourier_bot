from sqlalchemy import Column, Integer, VARCHAR, DATE, Identity, TIMESTAMP, BOOLEAN, BIGINT
from .base import Base

class Courier(Base):
    __tablename__ = "couriers"
    id = Column(Integer, Identity(start=1, cycle=True), primary_key=True)
    user_id = Column(BIGINT, unique=False, nullable=False)
    user_name = Column(VARCHAR(50), unique=False, nullable=False)
    city = Column(VARCHAR(20), unique=False, nullable=False)
    dest = Column(VARCHAR(20), unique=False, nullable=False)
    flight_date = Column(DATE, nullable=False)
    phone = Column(VARCHAR(20), unique=False, nullable=False)
    extra = Column(VARCHAR(120), unique=False, nullable=False)
    status = Column(BOOLEAN, nullable=False)

class Blacklist(Base):
    __tablename__ = "blacklist"
    id = Column('id', Integer, Identity(start=1, cycle=True), primary_key=True)
    user_id = Column('user_id', BIGINT, unique=False, nullable=False)

class Stats(Base):
    __tablename__ = "stats"
    id = Column('id', Integer, Identity(start=1, cycle=True), primary_key=True)
    user_id = Column('user_id', BIGINT, unique=True, nullable=False)
    timestamp = Column('timestamp', TIMESTAMP(timezone=False), nullable=False)

class Stats_search(Base):
    __tablename__ = "stats_search"
    id = Column('id', Integer, Identity(start=1, cycle=True), primary_key=True)
    user_id = Column('user_id', BIGINT, unique=False, nullable=False)
    city_from = Column(VARCHAR(20), unique=False, nullable=False)
    city_to = Column(VARCHAR(20), unique=False, nullable=False)
    timestamp = Column('timestamp', TIMESTAMP(timezone=False), nullable=False)


    def __repr__(self):
        return "".format(self.code)
