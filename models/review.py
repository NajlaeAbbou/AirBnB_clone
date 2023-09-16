#!/usr/bin/python3
""" Review module for the AirBnb project """
from models.base_model import BaseModel


class Review(BaseModel):
    """ Review class """
    place_id = ""
    user_id = ""
    text = ""
