#!/usr/bin/python3
"""This module defines the Place class."""
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Table, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv
import models


place_amenity = Table("place_amenity", Base.metadata,
                      Column("place_id", String(60),
                             ForeignKey("places.id"),
                             primary_key=True,
                             nullable=False),
                      Column("amenity_id", String(60),
                             ForeignKey("amenities.id"),
                             primary_key=True,
                             nullable=False))


class Place(BaseModel, Base):
    """This class represents a place.

    Attributes:
        city_id (str): The id of the city where the place is located.
        user_id (str): The id of the user who owns the place.
        name (str): The name of the place.
        description (str): The description of the place.
        number_rooms (int): The number of rooms in the place.
        number_bathrooms (int): The number of bathrooms in the place.
        max_guest (int): The maximum number of guests the place can accommodate.
        price_by_night (int): The price per night for staying at the place.
        latitude (float): The latitude coordinate of the place.
        longitude (float): The longitude coordinate of the place.
        amenity_ids (list): The list of ids of amenities associated with the place.
    """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    amenity_ids = []

    if getenv("HBNB_TYPE_STORAGE") == "db":
        reviews = relationship("Review", cascade='all, delete, delete-orphan',
                               backref="place")

        amenities = relationship("Amenity", secondary=place_amenity,
                                 viewonly=False,
                                 back_populates="place_amenities")
    else:
        @property
        def reviews(self):
            """Get the list of reviews associated with the place."""
            all_instances = models.storage.all()
            reviews_list = []
            result = []
            for key in all_instances:
                instance = key.replace('.', ' ')
                instance = shlex.split(instance)
                if instance[0] == 'Review':
                    reviews_list.append(all_instances[key])
            for review in reviews_list:
                if review.place_id == self.id:
                    result.append(review)
            return result

        @property
        def amenities(self):
            """Get the list of amenity ids associated with the place."""
            return self.amenity_ids

        @amenities.setter
        def amenities(self, obj=None):
            """Set the list of amenity ids associated with the place."""
            if isinstance(obj, Amenity) and obj.id not in self.amenity_ids:
                self.amenity_ids.append(obj.id)

