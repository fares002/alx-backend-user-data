#!/usr/bin/env python3
"""SQLAlchemy model named User for a database table named users"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    """User model"""
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    hased_password = Column(String, nullable=False)
    session_id = Column(String, nullable=True)
    reset_token = Column(String, nullable=True)

    