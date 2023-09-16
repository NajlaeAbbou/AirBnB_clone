#!/usr/bin/python3
"""FileStorage class"""

import json
from models.base_model import BaseModel


class FileStorage:
    """Serializes inst to a JSON file and deserializes
    JSON file to inst

    Attributes:
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
