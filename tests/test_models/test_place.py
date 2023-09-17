#!/usr/bin/python3
"""unittests pace.py"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.place import Place


class TestPlace_instantiation(unittest.TestCase):
    """Testing instantiation of the Place class"""

    def test_noargs_insta(self):
        self.assertEqual(Place, type(Place()))

    def test_new_inobjects(self):
        self.assertIn(Place(), models.storage.all().values())

    def test_id_str(self):
        self.assertEqual(str, type(Place().id))

    def test_created_at_datetime(self):
        self.assertEqual(datetime, type(Place().created_at))

    def test_updated_at_datetime(self):
        self.assertEqual(datetime, type(Place().updated_at))

    def test_city_id_isclass_attr(self):
        p = Place()
        self.assertEqual(str, type(Place.city_id))
        self.assertIn("city_id", dir(p))
        self.assertNotIn("city_id", p.__dict__)

    def test_user_id_class_attr(self):
        p = Place()
        self.assertEqual(str, type(Place.user_id))
        self.assertIn("user_id", dir(p))
        self.assertNotIn("user_id", p.__dict__)

    def test_name_class_attr(self):
        p = Place()
        self.assertEqual(str, type(Place.name))
        self.assertIn("name", dir(p))
        self.assertNotIn("name", p.__dict__)

    def test_description_class_att(self):
        p = Place()
        self.assertEqual(str, type(Place.description))
        self.assertIn("description", dir(p))
        self.assertNotIn("desctiption", p.__dict__)

    def test_number_rooms_class_attr(self):
        p = Place()
        self.assertEqual(int, type(Place.number_rooms))
        self.assertIn("number_rooms", dir(p))
        self.assertNotIn("number_rooms", p.__dict__)

    def test_number_bathrooms_class_attr(self):
        p = Place()
        self.assertEqual(int, type(Place.number_bathrooms))
        self.assertIn("number_bathrooms", dir(p))
        self.assertNotIn("number_bathrooms", p.__dict__)

    def test_max_guest_class_attr(self):
        p = Place()
        self.assertEqual(int, type(Place.max_guest))
        self.assertIn("max_guest", dir(p))
        self.assertNotIn("max_guest", p.__dict__)

    def test_price_by_nightclass_attr(self):
        p = Place()
        self.assertEqual(int, type(Place.price_by_night))
        self.assertIn("price_by_night", dir(p))
        self.assertNotIn("price_by_night", p.__dict__)

    def test_latitude_class_attr(self):
        p = Place()
        self.assertEqual(float, type(Place.latitude))
        self.assertIn("latitude", dir(p))
        self.assertNotIn("latitude", p.__dict__)

    def test_longitude_class_attr(self):
        p = Place()
        self.assertEqual(float, type(Place.longitude))
        self.assertIn("longitude", dir(p))
        self.assertNotIn("longitude", p.__dict__)

    def test_amenity_ids_class_attr(self):
        p = Place()
        self.assertEqual(list, type(Place.amenity_ids))
        self.assertIn("amenity_ids", dir(p))
        self.assertNotIn("amenity_ids", p.__dict__)

    def test_unique_ids(self):
        pl1 = Place()
        pl2 = Place()
        self.assertNotEqual(pl1.id, pl2.id)

    def test_different_created_at(self):
        pl1 = Place()
        sleep(0.3)
        pl2 = Place()
        self.assertLess(pl1.created_at, pl2.created_at)

    def test_different_updated_at(self):
        pl1 = Place()
        sleep(0.3)
        pl2 = Place()
        self.assertLess(pl1.updated_at, pl2.updated_at)

    def test_str_repr(self):
        t = datetime.now()
        trepr = repr(t)
        p = Place()
        p.id = "120"
        p.created_at = p.updated_at = t
        pstr = p.__str__()
        self.assertIn("[Place] (120)", pstr)
        self.assertIn("'id': '120'", pstr)
        self.assertIn("'created_at': " + trepr, pstr)
        self.assertIn("'updated_at': " + trepr, pstr)

    def test_args(self):
        p = Place(None)
        self.assertNotIn(None, p.__dict__.values())

    def test_insta_kwargs(self):
        t = datetime.now()
        isot = t.isoformat()
        p = Place(id="789", created_at=isot, updated_at=isot)
        self.assertEqual(p.id, "789")
        self.assertEqual(p.created_at, t)
        self.assertEqual(p.updated_at, t)

    def test_inst_nokwargs(self):
        with self.assertRaises(TypeError):
            Place(id=None, created_at=None, updated_at=None)


class TestPlace_to_dict(unittest.TestCase):
    """Test to_dict method"""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(Place().to_dict()))

    def test_to_dict_keys(self):
        p = Place()
        self.assertIn("id", p.to_dict())
        self.assertIn("created_at", p.to_dict())
        self.assertIn("updated_at", p.to_dict())
        self.assertIn("__class__", p.to_dict())

    def test_to_dict_added_attr(self):
        p = Place()
        p.middle_name = "Tangier"
        p.my_number = 25
        self.assertEqual("Tangier", p.middle_name)
        self.assertIn("my_number", p.to_dict())

    def test_to_dict_datetime_attstrs(self):
        p = Place()
        p_dict = p.to_dict()
        self.assertEqual(str, type(p_dict["id"]))
        self.assertEqual(str, type(p_dict["created_at"]))
        self.assertEqual(str, type(p_dict["updated_at"]))

    def test_to_dict_output(self):
        t = datetime.now()
        p = Place()
        p.id = "120"
        p.created_at = p.updated_at = t
        tdict = {
            'id': '120',
            '__class__': 'Place',
            'created_at': t.isoformat(),
            'updated_at': t.isoformat(),
        }
        self.assertDictEqual(p.to_dict(), tdict)

    def test_cont_to_dict(self):
        p = Place()
        self.assertNotEqual(p.to_dict(), p.__dict__)

    def test_to_dic_arg(self):
        p = Place()
        with self.assertRaises(TypeError):
            p.to_dict(None)


class TestPlace_save(unittest.TestCase):
    """Testing save method of the Place class"""

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

    def test_one_save(self):
        p = Place()
        sleep(0.3)
        first_updated_at = p.updated_at
        p.save()
        self.assertLess(first_updated_at, p.updated_at)

    def test_two_saves(self):
        p = Place()
        sleep(0.3)
        first_updated_at = p.updated_at
        p.save()
        second_updated_at = p.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.3)
        p.save()
        self.assertLess(second_updated_at, p.updated_at)

    def test_save_with_arg(self):
        p = Place()
        with self.assertRaises(TypeError):
            p.save(None)

    def test_save_updates_file(self):
        p = Place()
        p.save()
        pid = "Place." + p.id
        with open("file.json", "r") as f:
            self.assertIn(pid, f.read())


if __name__ == "__main__":
    unittest.main()
