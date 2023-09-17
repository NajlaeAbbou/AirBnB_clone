#!/usr/bin/python3
"""Unittests for file_storage.py"""
import json
import models
import os
import unittest
from datetime import datetime
from models.engine.file_storage import FileStorage


class mmethods_FileStorage(unittest.TestCase):
    """Testing methods FileStorage"""
    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

    def aall(self):
        self.assertEqual(dict, type(models.storage.all()))

    def aall_arg(self):
        with self.assertRaises(TypeError):
            models.storage.all(None)

    def _new(self):
        b = BaseModel()
        u = User()
        s = State()
        p = Place()
        c = City()
        a = Amenity()
        r = Review()
        models.storage.new(b)
        models.storage.new(u)
        models.storage.new(s)
        models.storage.new(p)
        models.storage.new(c)
        models.storage.new(a)
        models.storage.new(r)
        self.assertIn("BaseModel." + b.id, models.storage.all().keys())
        self.assertIn(b, models.storage.all().values())
        self.assertIn("User." + u.id, models.storage.all().keys())
        self.assertIn(u, models.storage.all().values())
        self.assertIn("State." + s.id, models.storage.all().keys())
        self.assertIn(s, models.storage.all().values())
        self.assertIn("Place." + p.id, models.storage.all().keys())
        self.assertIn(p, models.storage.all().values())
        self.assertIn("City." + c.id, models.storage.all().keys())
        self.assertIn(c, models.storage.all().values())
        self.assertIn("Amenity." + a.id, models.storage.all().keys())
        self.assertIn(a, models.storage.all().values())
        self.assertIn("Review." + r.id, models.storage.all().keys())
        self.assertIn(r, models.storage.all().values())

    def nnew_args(self):
        with self.assertRaises(TypeError):
            models.storage.new(BaseModel(), 23)

     def _reload(self):
        b = BaseModel()
        u = User()
        s = State()
        p = Place()
        c = City()
        a = Amenity()
        r = Review()
        models.storage.new(b)
        models.storage.new(u)
        models.storage.new(s)
        models.storage.new(p)
        models.storage.new(c)
        models.storage.new(a)
        models.storage.new(r)
        models.storage.save()
        models.storage.reload()
        neww = FileStorage._FileStorage__objects
        self.assertIn("BaseModel." + b.id, neww)
        self.assertIn("User." + u.id, neww
        self.assertIn("State." + s.id, neww)
        self.assertIn("Place." + p.id, neww)
        self.assertIn("City." + c.id, neww)
        self.assertIn("Amenity." + a.id, neww)
        self.assertIn("Review." + r.id, neww)

    def rreload_arg(self):
        with self.assertRaises(TypeError):
            models.storage.reload(None)

    def _save(self):
        b = BaseModel()
        u = User()
        s = State()
        p = Place()
        c = City()
        a = Amenity()
        r = Review()
        models.storage.new(b)
        models.storage.new(u)
        models.storage.new(s)
        models.storage.new(p)
        models.storage.new(c)
        models.storage.new(a)
        models.storage.new(r)
        models.storage.save()
        neww = ""
        with open("file.json", "r") as f:
            neww = f.read()
            self.assertIn("BaseModel." + b.id, save_text)
            self.assertIn("User." + u.id, neww)
            self.assertIn("State." + s.id, neww)
            self.assertIn("Place." + p.id, neww)
            self.assertIn("City." + c.id, neww)
            self.assertIn("Amenity." + a.id, neww)
            self.assertIn("Review." + r.id, neww)

    def ssave_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.save(None)

class iinit__FileStorage(unittest.TestCase):
    """insti filestorage class"""

    def ssstorage(self):
        self.assertEqual(type(models.storage), FileStorage)

    def FFileStorage_file_path(self):
        self.assertEqual(str, type(FileStorage._FileStorage__file_path))

    def FFileStorage_no_args(self):
        self.assertEqual(type(FileStorage()), FileStorage)

     def testFileStorageobjects(self):
        self.assertEqual(dict, type(FileStorage._FileStorage__objects))

     def FFileStorage_arg(self):
        with self.assertRaises(TypeError):
            FileStorage(None)


if __name__ == "__main__":
    unittest.main()
