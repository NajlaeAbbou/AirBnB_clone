#!/usr/bin/python3
"""FileStorage class"""

import json
import os
import datetime
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """Serializes inst to a JSON file and deserializes
    JSON file to inst
    Args:
        __file_path : path to JSON file
        __objects : store all in <class name>.id
    """

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns objects"""
        return FileStorage.__objects

    def new(self, obj):
        """Sets in objects of the obj with <obj_class_name>.id"""
        cname = obj.__class__.__name__
        FileStorage.__objects["{}.{}".format(cname, obj.id)] = obj

    def save(self):
        """Serializes objects to JSON file"""
        diction = FileStorage.__objects
        odiction = {obj: diction[obj].to_dict() for obj in diction.keys()}
        with open(FileStorage.__file_path, "w") as f:
            json.dump(odiction, f)

    def reload(self):
        """Deserializes the JSON file to objects"""
        try:
            with open(FileStorage.__file_path) as f:
                for ob in json.load(f).values():
                    cname = ob["__class__"]
                    del ob["__class__"]
                    self.new(eval(cname)(**ob))
        except FileNotFoundError:
            return

    def attributes(self):
        """Returns the valid att and their types for class."""
        attributes = {
            "BaseModel":
                     {"id": str,
                      "created_at": datetime.datetime,
                      "updated_at": datetime.datetime},
            "User":
                     {"email": str,
                      "password": str,
                      "first_name": str,
                      "last_name": str},
            "State":
                     {"name": str},
            "City":
                     {"state_id": str,
                      "name": str},
            "Amenity":
                     {"name": str},
            "Place":
                     {"city_id": str,
                      "user_id": str,
                      "name": str,
                      "description": str,
                      "number_rooms": int,
                      "number_bathrooms": int,
                      "max_guest": int,
                      "price_by_night": int,
                      "latitude": float,
                      "longitude": float,
                      "amenity_ids": list},
            "Review":
            {"place_id": str,
                         "user_id": str,
                         "text": str}
        }
        return attributes

    def classes(self):
        """Returns a dictionary."""

        classes = {"BaseModel": BaseModel,
                   "User": User,
                   "State": State,
                   "City": City,
                   "Amenity": Amenity,
                   "Place": Place,
                   "Review": Review}
        return classes
