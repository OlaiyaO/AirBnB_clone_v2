#!/usr/bin/python3
""" new class for sqlAlchemy """
from os import getenv
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import (create_engine)
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class DBStorage:
    """Manage SQL Alchemy database."""
    __engine = None
    __session = None

    def __init__(self):
        user_name = getenv("HBNB_MYSQL_USER")
        password = getenv("HBNB_MYSQL_PWD")
        db_name = getenv("HBNB_MYSQL_DB")
        host_name = getenv("HBNB_MYSQL_HOST")
        env_var = getenv("HBNB_ENV")

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(user_name, password, host_name, db_name),
                                      pool_pre_ping=True)

        if env_var == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Get all objects from database."""
        obj_dict = {}
        if cls:
            if type(cls) is str:
                cls = eval(cls)
            query = self.__session.query(cls)
            for obj in query:
                key = "{}.{}".format(type(obj).__name__, obj.id)
                obj_dict[key] = obj
        else:
            class_list = [State, City, User, Place, Review, Amenity]
            for obj in class_list:
                query = self.__session.query(obj)
                for obj in query:
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    obj_dict[key] = obj
        return (obj_dict)

    def new(self, obj):
        """Add new object to database."""
        self.__session.add(obj)

    def save(self):
        """Save changes to the database."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete an object from the database."""
        if obj:
            self.session.delete(obj)

    def reload(self):
        """Reload the database."""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Close the database connection."""
        self.__session.close()
