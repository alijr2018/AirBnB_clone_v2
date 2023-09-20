#!/usr/bin/python3
"""This module defines a class User"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """
    Definition of the User class for the users table in
    the database.
    Args:
        BaseModel (class): the BaseModel class.
        Base (class): the declarative Base class from SQLAlchemy.
    """

    __tablename__ = 'users'

    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128))
    last_name = Column(String(128))
    # places = relationship('Place', back_populates='user',
    #                       cascade='all, delete-orphan')
    # reviews = relationship('Review', back_populates='user',
    #                        cascade='all, delete-orphan')
