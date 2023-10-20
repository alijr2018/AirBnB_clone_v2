#!/usr/bin/python3
""" State Module for HBNB project """

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv
from models import storage
from models.city import City


class State(BaseModel, Base):
    """State class"""
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        cities = relationship("City", backref="state", cascade="all, delete")

    else:
        @property
        def cities(self):
            """
            Returns the list of City instances with state_id
            equal to the current State.id
            """
            cities = storage.all(City)
            return ([city for city in cities.values() if city.state_id == self.id])
