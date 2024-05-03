#!/usr/bin/python3
"""This is the amenity class implementation"""
from models.base_model import BaseModel, Base
from models.place import place_amenity
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """This is the class definition of Amenity
    """
    __tablename__ = "amenities"
    name = Column(String(128), nullable=False)
    place_amenities = relationship("Place", secondary=place_amenity)
