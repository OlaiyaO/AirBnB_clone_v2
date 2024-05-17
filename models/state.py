#!/usr/bin/python3
"""This module defines the State class."""
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
import models
from models.city import City
import shlex


class State(BaseModel, Base):
    """This class represents a state.

    Attributes:
        name (str): The name of the state.
        cities (relationship): The relationship between the state and cities.
    """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship("City", cascade='all, delete, delete-orphan',
                          backref="state")

    @property
    def cities(self):
        """Get the list of cities associated with the state."""
        all_instances = models.storage.all()
        cities_list = []
        result = []
        for key in all_instances:
            instance = key.replace('.', ' ')
            instance = shlex.split(instance)
            if instance[0] == 'City':
                cities_list.append(all_instances[key])
        for city in cities_list:
            if city.state_id == self.id:
                result.append(city)
        return result
