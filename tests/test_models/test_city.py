#!/usr/bin/python3
"""unitests for class city.py
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.city import City


class TestCity_instantiation(unittest.TestCase):
    """test insta city"""

    def test_noargs_insta(self):
        self.assertEqual(City, type(City()))

    def test_newstored(self):
        self.assertIn(City(), models.storage.all().values())

    def test_id_str(self):
        self.assertEqual(str, type(City().id))

    def test_created_at_datetime(self):
        self.assertEqual(datetime, type(City().created_at))

    def test_updated_at_datetime(self):
        self.assertEqual(datetime, type(City().updated_at))

    def test_state_id_class_att(self):
        c = City()
        self.assertEqual(str, type(City.state_id))
        self.assertIn("state_id", dir(c))
        self.assertNotIn("state_id", c.__dict__)

    def test_name_class_att(self):
        c = City()
        self.assertEqual(str, type(City.name))
        self.assertIn("name", dir(c))
        self.assertNotIn("name", c.__dict__)

    def test_unique_ids(self):
        cc = City()
        cc2 = City()
        self.assertNotEqual(cc.id, cc2.id)

    def test_diff_created_at(self):
        cc = City()
        sleep(0.6)
        cc2 = City()
        self.assertLess(cc.created_at, cc2.created_at)

    def test_different_updated_at(self):
        cc = City()
        sleep(0.4)
        cc2 = City()
        self.assertLess(cc.updated_at, cc2.updated_at)

    def test_str_repr(self):
        t = datetime.today()
        trepr = repr(t)
        c = City()
        c.id = "786"
        c.created_at = c.updated_at = t
        cs = c.__str__()
        self.assertIn("[City] (786)", cs)
        self.assertIn("'id': '786'", cs)
        self.assertIn("'created_at': " + trepr, cs)
        self.assertIn("'updated_at': " + trepr, cs)

    def test_noargs(self):
        c = City(None)
        self.assertNotIn(None, c.__dict__.values())

    def test_insta_kwargs(self):
        t = datetime.today()
        isot = t.isoformat()
        c = City(id="785", created_at=isot, updated_at=isot)
        self.assertEqual(c.id, "785")
        self.assertEqual(c.created_at, t)
        self.assertEqual(c.updated_at, t)

    def test_insta_nokwargs(self):
        with self.assertRaises(TypeError):
            City(id=None, created_at=None, updated_at=None)


class TestCity_save(unittest.TestCase):
    """test save method of City class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_save(self):
        c = City()
        sleep(0.3)
        fupdated_at = c.updated_at
        c.save()
        self.assertLess(fupdated_at, c.updated_at)

    def test_tsaves(self):
        c = City()
        sleep(0.3)
        fupdated_at = c.updated_at
        c.save()
        supdated_at = c.updated_at
        self.assertLess(fupdated_at, supdated_at)
        sleep(0.3)
        c.save()
        self.assertLess(supdated_at, c.updated_at)

    def test_save_arg(self):
        c = City()
        with self.assertRaises(TypeError):
            c.save(None)

    def test_save_updatefile(self):
        c = City()
        c.save()
        cid = "City." + c.id
        with open("file.json", "r") as f:
            self.assertIn(cid, f.read())


class TestCity_to_dict(unittest.TestCase):
    """test to_dict method City class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(City().to_dict()))

    def test_to_dict_keys(self):
        c = City()
        self.assertIn("id", c.to_dict())
        self.assertIn("created_at", c.to_dict())
        self.assertIn("updated_at", c.to_dict())
        self.assertIn("__class__", c.to_dict())

    def test_to_dict_attr(self):
        c = City()
        c.middle_name = "Najlae"
        c.my_number = 29
        self.assertEqual("Najlae", c.middle_name)
        self.assertIn("my_number", c.to_dict())

    def test_to_dict_datetime_attrstr(self):
        c = City()
        c_dict = c.to_dict()
        self.assertEqual(str, type(c_dict["id"]))
        self.assertEqual(str, type(c_dict["created_at"]))
        self.assertEqual(str, type(c_dict["updated_at"]))

    def test_to_dict_output(self):
        t = datetime.today()
        c = City()
        c.id = "786"
        c.created_at = c.updated_at = t
        tdict = {
            'id': '786',
            '__class__': 'City',
            'created_at': t.isoformat(),
            'updated_at': t.isoformat(),
        }
        self.assertDictEqual(c.to_dict(), tdict)

    def test_cont_to_dict(self):
        c = City()
        self.assertNotEqual(c.to_dict(), c.__dict__)

    def test_to_dict_arg(self):
        c = City()
        with self.assertRaises(TypeError):
            c.to_dict(None)


if __name__ == "__main__":
    unittest.main()
