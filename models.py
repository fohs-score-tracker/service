from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .database import Base

# add to this list whenever a new class gets added


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(Text, unique=True)
    username = Column(Text, unique=True)
    full_name = Column(Text)
    pw_hash = Column(Text)
    pw_salt = Column(Text)
   # Players = relationship("Player", back_populates="User")

class Player(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True)
    full_name = Column(Text, nullable=False)
    username = Column(Text, unique=True)
    two_pointers = Column(Integer, default=0, nullable=False)
    missed_two_pointers = Column(Integer, default=0, nullable=False)
    three_pointers = Column(Integer, default=0, nullable=False)
    missed_three_pointers = Column(Integer, default=0, nullable=False)
  #  User = relationship("User", back_populates="Players")