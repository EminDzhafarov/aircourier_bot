from sqlalchemy import Column, Integer, VARCHAR, DATE, Identity, TIMESTAMP, BOOLEAN, BIGINT
from .base import Base

# Список курьеров
class Courier(Base):
    __tablename__ = "couriers"
    id = Column(Integer, nullable=False, unique=True, primary_key=True)
    user_id = Column(BIGINT, unique=False, nullable=False)
    user_name = Column(VARCHAR(50), unique=False, nullable=False)
    city_from = Column(VARCHAR(25), unique=False, nullable=False)
    city_to = Column(VARCHAR(25), unique=False, nullable=False)
    flight_date = Column(DATE, nullable=False)
    phone = Column(VARCHAR(20), unique=False, nullable=False)
    info = Column(VARCHAR(200), unique=False, nullable=False)
    status = Column(BOOLEAN, nullable=False)

# Черный список
class Blacklist(Base):
    __tablename__ = "blacklist"
    user_id = Column(BIGINT, unique=True, nullable=False, primary_key=True)

# Уникальные пользователи
class Stats(Base):
    __tablename__ = "stats"
    user_id = Column(BIGINT, unique=True, nullable=False, primary_key=True)
    timestamp = Column(TIMESTAMP(timezone=False), nullable=False)

# История поиска
class Stats_search(Base):
    __tablename__ = "stats_search"
    user_id = Column(BIGINT, unique=False, nullable=False, primary_key=True)
    city_from = Column(VARCHAR(20), unique=False, nullable=False)
    city_to = Column(VARCHAR(20), unique=False, nullable=False)
    timestamp = Column(TIMESTAMP(timezone=False), nullable=False)

# Администраторы
class Admins(Base):
    __tablename__ = "admins"
    user_id = Column(BIGINT, unique=True, nullable=True, primary_key=True)