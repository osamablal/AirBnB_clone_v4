#!/usr/bin/python3
"""
The Data-base Storage of engine.
"""

import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models import base_model, amenity, city, place, review, state, user


class DBStorage:
    """
        Getting along with long storage for instences.
    """
    CNC = {
        'Amenity': amenity.Amenity,
        'City': city.City,
        'Place': place.Place,
        'Review': review.Review,
        'State': state.State,
        'User': user.User
    }

    """
        Getting along with storage of Data-base.
    """
    __engine = None
    __session = None

    def __init__(self):
        """
            Initiating the engine.
        """
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(
                os.environ.get('HBNB_MYSQL_USER'),
                os.environ.get('HBNB_MYSQL_PWD'),
                os.environ.get('HBNB_MYSQL_HOST'),
                os.environ.get('HBNB_MYSQL_DB')))
        if os.environ.get("HBNB_ENV") == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
           Giving back dictienary of objects.
        """
        obj_dict = {}
        if cls is not None:
            a_query = self.__session.query(DBStorage.CNC[cls])
            for obj in a_query:
                obj_ref = "{}.{}".format(type(obj).__name__, obj.id)
                obj_dict[obj_ref] = obj
            return obj_dict

        for c in DBStorage.CNC.values():
            a_query = self.__session.query(c)
            for obj in a_query:
                obj_ref = "{}.{}".format(type(obj).__name__, obj.id)
                obj_dict[obj_ref] = obj
        return obj_dict

    def new(self, obj):
        """
            Adding objects to currant data-base.
        """
        self.__session.add(obj)

    def save(self):
        """
            Commiting changes of the current data-base.
        """
        self.__session.commit()

    def rollback_session(self):
        """
            Going back the session to exception event.
        """
        self.__session.rollback()

    def delete(self, obj=None):
        """
            Deleting objects from current data-base.
        """
        if obj:
            self.__session.delete(obj)
            self.save()

    def delete_all(self):
        """
           Deleting all storage objects.
        """
        for c in DBStorage.CNC.values():
            a_query = self.__session.query(c)
            all_objs = [obj for obj in a_query]
            for obj in range(len(all_objs)):
                to_delete = all_objs.pop(0)
                to_delete.delete()
        self.save()

    def reload(self):
        """
           Reloading back the data-base.
        """
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(
            sessionmaker(
                bind=self.__engine,
                expire_on_commit=False))

    def close(self):
        """
            Calling the remove fun.
        """
        self.__session.remove()

    def get(self, cls, id):
        """
            Giving or getting back an object.
        """
        if cls and id:
            fetch = "{}.{}".format(cls, id)
            all_obj = self.all(cls)
            return all_obj.get(fetch)
        return None

    def count(self, cls=None):
        """
            Giving back the num of all objects.
        """
        return (len(self.all(cls)))
