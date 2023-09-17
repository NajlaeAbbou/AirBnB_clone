#!/usr/bin/python3
"""unittests amenity.py"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.amenity import Amenity


class TestAmenity_instantiation(unittest.TestCase):
    """test instantiation of Amenity class."""

    def test_noargs_insta(self):
        self.assertEqual(Amenity, type(Amenity()))

    def test_inst_stored(self):
        self.assertIn(Amenity(), models.storage.all().values())

    def test_id_str(self):
        self.assertEqual(str, type(Amenity().id))

    def test_created_at_datetime(self):
        self.assertEqual(datetime, type(Amenity().created_at))

    def test_updated_at_datetime(self):
        self.assertEqual(datetime, type(Amenity().updated_at))

    def test_name_class_attribute(self):
        m = Amenity()
        self.assertEqual(str, type(Amenity.name))
        self.assertIn("name", dir(Amenity()))
        self.assertNotIn("name", m.__dict__)

    def test_unique_ids(self):
        am1 = Amenity()
        am2 = Amenity()
        self.assertNotEqual(am1.id, am2.id)

    def test_different_created_at(self):
        am1 = Amenity()
        sleep(0.1)
        am2 = Amenity()
        self.assertLess(am1.created_at, am2.created_at)

    def test_different_updated_at(self):
        am1 = Amenity()
        sleep(0.2)
        am2 = Amenity()
        self.assertLess(am1.updated_at, am2.updated_at)

    def test_str_repr(self):
        t = datetime.today()
        t_repr = repr(t)
        m = Amenity()
        m.id = "456"
        m.created_at = m.updated_at = t
        ms = m.__str__()
        self.assertIn("[Amenity] (456)", ms)
        self.assertIn("'id': '456'", ms)
        self.assertIn("'created_at': " + t_repr, ms)
        self.assertIn("'updated_at': " + t_repr, ms)

    def test_noargs(self):
        m = Amenity(None)
        self.assertNotIn(None, m.__dict__.values())

    def test_insta_kwargs(self):
        t = datetime.today()
        isot = t.isoformat()
        m = Amenity(id="520", created_at=isot, updated_at=isot)
        self.assertEqual(m.id, "520")
        self.assertEqual(m.created_at, t)
        self.assertEqual(m.updated_at, t)

    def test_insta_nokwargs(self):
        with self.assertRaises(TypeError):
            Amenity(id=None, created_at=None, updated_at=None)


class TestAmenity_save(unittest.TestCase):
    """test save method Amenity class."""

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
        m = Amenity()
        sleep(0.2)
        fupdated_at = m.updated_at
        m.save()
        self.assertLess(fupdated_at, m.updated_at)

    def test_twsaves(self):
        m = Amenity()
        sleep(0.3)
        fupdated_at = m.updated_at
        m.save()
        supdated_at = m.updated_at
        self.assertLess(fupdated_at, supdated_at)
        sleep(0.5)
        m.save()
        self.assertLess(supdated_at, m.updated_at)

    def test_save_with_arg(self):
        m = Amenity()
        with self.assertRaises(TypeError):
            m.save(None)

    def test_saveupdates_file(self):
        m = Amenity()
        m.save()
        amid = "Amenity." + m.id
        with open("file.json", "r") as f:
            self.assertIn(amid, f.read())


class TestAmenity_to_dict(unittest.TestCase):
    """test to_dict method of  Amenity class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(Amenity().to_dict()))

    def test_to_dict_keys(self):
        m = Amenity()
        self.assertIn("id", m.to_dict())
        self.assertIn("created_at", m.to_dict())
        self.assertIn("updated_at", m.to_dict())
        self.assertIn("__class__", m.to_dict())

    def test_to_dict_attributes(self):
        m = Amenity()
        m.middle_name = "Najlae"
        m.my_number = 25
        self.assertEqual("Najlae", m.middle_name)
        self.assertIn("my_number", m.to_dict())

    def test_to_dict_datetime_strs(self):
        m = Amenity()
        am_dict = m.to_dict()
        self.assertEqual(str, type(am_dict["id"]))
        self.assertEqual(str, type(am_dict["created_at"]))
        self.assertEqual(str, type(am_dict["updated_at"]))

    def test_to_dict_output(self):
        t = datetime.today()
        m = Amenity()
        m.id = "189"
        m.created_at = m.updated_at = t
        tdict = {
            'id': '189',
            '__class__': 'Amenity',
            'created_at': t.isoformat(),
            'updated_at': t.isoformat(),
        }
        self.assertDictEqual(m.to_dict(), tdict)

    def test_cont_to_dict(self):
        m = Amenity()
        self.assertNotEqual(m.to_dict(), m.__dict__)

    def test_to_dict_arg(self):
        m = Amenity()
        with self.assertRaises(TypeError):
            m.to_dict(None)


if __name__ == "__main__":
    unittest.main()
