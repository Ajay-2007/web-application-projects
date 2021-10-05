from sqlalchemy import Boolean, TEXT, DECIMAL, Column, Integer, String, DateTime
import datetime

from database import Base


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True)
    name = Column(String)


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(TEXT)
    price = Column(DECIMAL(scale=2))
    available = Column(Boolean, default=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    updated = Column(DateTime, onupdate=datetime.datetime.now)