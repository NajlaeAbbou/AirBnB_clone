#!/usr/bin/python3
"""unittests for models/user.py.basemodel methods"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.user import User


class TestUser_instan(unittest.TestCase):
    """Unittests inst of the User class."""

    def test_no_args_instan(self):
        self.assertEqual(User, type(User()))

    def test_new_instance_inobjects(self):
        self.assertIn(User(), models.storage.all().values())

    def test_id_str(self):
        self.assertEqual(str, type(User().id))

    def test_created_at_datetime(self):
        self.assertEqual(datetime, type(User().created_at))

    def test_updated_at_datetime(self):
        self.assertEqual(datetime, type(User().updated_at))

    def test_email_str(self):
        self.assertEqual(str, type(User.email))

    def test_password_str(self):
        self.assertEqual(str, type(User.password))

    def test_first_name_str(self):
        self.assertEqual(str, type(User.first_name))

    def test_last_name_str(self):
        self.assertEqual(str, type(User.last_name))

    def test_conflict_ids(self):
        id1 = User()
        id2 = User()
        self.assertNotEqual(id1.id, id2.id)

    def test_diffrent_created_at(self):
        c1 = User()
        sleep(0.1)
        c2 = User()
        self.assertLess(c1.created_at, c2.created_at)

    def test_different_updated_at(self):
        u1 = User()
        sleep(0.2)
        u2 = User()
        self.assertLess(u1.updated_at, u2.updated_at)

    def test_str_representation(self):
        t = datetime.now()
        trepr = repr(t)
        u = User()
        u.id = "7584"
        u.created_at = u.updated_at = t
        us = u.__str__()
        self.assertIn("[User] (7584)", us)
        self.assertIn("'id': '7584'", us)
        self.assertIn("'created_at': " + trepr, us)
        self.assertIn("'updated_at': " + trepr, us)

    def test_no_args(self):
        u = User(None)
        self.assertNotIn(None, u.__dict__.values())

    def test_insta_kwargs(self):
        t = datetime.now()
        isot = t.isoformat()
        u = User(id="672", created_at=isot, updated_at=isot)
        self.assertEqual(u.id, "672")
        self.assertEqual(u.created_at, t)
        self.assertEqual(u.updated_at, t)

    def test_insta_No_kwargs(self):
        with self.assertRaises(TypeError):
            User(id=None, created_at=None, updated_at=None)


class TestUser_save(unittest.TestCase):
    """testing save method for USER."""

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
        u = User()
        sleep(0.3)
        fupdated_at = u.updated_at
        u.save()
        self.assertLess(fupdated_at, u.updated_at)

    def test_manysaves(self):
        u = User()
        sleep(0.3)
        fupdated_at = u.updated_at
        u.save()
        supdated_at = u.updated_at
        self.assertLess(fupdated_at, supdated_at)
        sleep(0.23)
        u.save()
        self.assertLess(supdated_at, u.updated_at)

    def test_save_arg(self):
        u = User()
        with self.assertRaises(TypeError):
            u.save(None)

    def test_save_updates_file(self):
        u = User()
        u.save()
        id1 = "User." + u.id
        with open("file.json", "r") as f:
            self.assertIn(id1, f.read())


class TestUser_to_dict(unittest.TestCase):
    """testing to_dict method USER."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(User().to_dict()))

    def test_to_dict_with_keys(self):
        u = User()
        self.assertIn("id", u.to_dict())
        self.assertIn("created_at", u.to_dict())
        self.assertIn("updated_at", u.to_dict())
        self.assertIn("__class__", u.to_dict())

    def test_to_dict_with_values(self):
        u = User()
        u.middle_name = "vache"
        u.my_number = 566
        self.assertEqual("vache", u.middle_name)
        self.assertIn("my_number", u.to_dict())

    def test_to_dict_datetime_string(self):
        u = User()
        diction = u.to_dict()
        self.assertEqual(str, type(diction["id"]))
        self.assertEqual(str, type(diction["created_at"]))
        self.assertEqual(str, type(diction["updated_at"]))

    def test_to_dict_output(self):
        t = datetime.now()
        u = User()
        u.id = "2637"
        u.created_at = u.updated_at = t
        diction1 = {
            'id': '2637',
            '__class__': 'User',
            'created_at': t.isoformat(),
            'updated_at': t.isoformat(),
        }
        self.assertDictEqual(u.to_dict(), diction1)

    def test_contr_dict(self):
        u = User()
        self.assertNotEqual(u.to_dict(), u.__dict__)

    def test_to_dict_with_arg(self):
        u = User()
        with self.assertRaises(TypeError):
            u.to_dict(None)


if __name__ == "__main__":
    unittest.main()
