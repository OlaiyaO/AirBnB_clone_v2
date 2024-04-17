#!/usr/bin/python3
"""Class for managing SQL Alchemy database."""
from os import getenv
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity

class DatabaseStorage:
    """Manage SQL Alchemy database."""
    __db_engine = None
    __db_session = None

    def __init__(self):
        """Initialize database connection."""
        user = getenv("HBNB_DB_USER")
        passwd = getenv("HBNB_DB_PASSWORD")
        db = getenv("HBNB_DB_NAME")
        host = getenv("HBNB_DB_HOST")
        env = getenv("HBNB_ENVIRONMENT")

        self.__db_engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                         .format(user, passwd, host, db),
                                         pool_pre_ping=True)

        if env == "test":
            Base.metadata.drop_all(self.__db_engine)

    def get_all(self, cls=None):
        """Get all objects from database."""
        obj_dict = {}
        if cls:
            if type(cls) is str:
                cls = eval(cls)
            query = self.__db_session.query(cls)
            for obj in query:
                key = "{}.{}".format(type(obj).__name__, obj.id)
                obj_dict[key] = obj
        else:
            classes = [State, City, User, Place, Review, Amenity]
            for cls in classes:
                query = self.__db_session.query(cls)
                for obj in query:
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    obj_dict[key] = obj
        return obj_dict

    def add(self, obj):
        """Add new object to database."""
        self.__db_session.add(obj)

    def save(self):
        """Save changes to the database."""
        self.__db_session.commit()

    def delete(self, obj=None):
        """Delete an object from the database."""
        if obj:
            self.__db_session.delete(obj)

    def reload(self):
        """Reload the database."""
        Base.metadata.create_all(self.__db_engine)
        session_factory = sessionmaker(bind=self.__db_engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__db_session = Session()

    def close(self):
        """Close the database connection."""
        self.__db_session.close()

