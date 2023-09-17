#!/usr/bin/python3
"""the base model class"""

from uuid import uuid4
import models
from datetime import datetime


class BaseModel:
    """attributes and methods of basemodel class"""
    def __init__(self, *args, **kwargs):
        """Initialization of BaseModel
        Args:
            *args: List of arguments
            **kwargs (dict): Key/value of attributes
        """
        self.id = str(uuid4())
        self.created_at = datetime.today()
        self.updated_at = datetime.today()
        tformat = "%Y-%m-%dT%H:%M:%S.%f"
        if len(kwargs) != 0:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    self.__dict__[key] = datetime.strptime(value, tformat)
                else:
                    self.__dict__[key] = value
        else:
            models.storage.new(self)

    def __str__(self):
        """string representation of the instance"""

        return "[{}] ({}) {}".format(
            self.__class__.__name__,
            self.id,
            self.__dict__
            )

    def save(self):
        """Save updates to update_at"""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """Returns a key/value representation of an instance"""
        dictionnary = self.__dict__.copy()
        dictionnary["__class__"] = self.__class__.__name__
        dictionnary["created_at"] = self.created_at.isoformat()
        dictionnary["updated_at"] = self.updated_at.isoformat()
        return dictionnary
