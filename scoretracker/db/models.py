"""
Database model classes.
"""

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from .connection import Base, engine


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)  # TODO: hash passwords

    # items = relationship("Item", back_populates="owner")

class Player(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key= True, index=True)
    full_name = Column(String)
    two_pointers = Column(Integer, default= 0, nullable=False)
    missed_two_pointers = Column(Integer, default=0, nullable=False)
    three_pointers = Column(Integer, default=0, nullable=False)
    missed_three_pointers = Column(Integer, default=0, nullable=False)
