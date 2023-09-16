#!/usr/bin/python3
"""unittests for models/base_model.py"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.base_model import BaseModel


class TestBaseModel_instantiation(unittest.TestCase):
    """Instantiation of the BaseModel class"""

    def test_noargs_instant(self):
        self.assertEqual(BaseModel, type(BaseModel()))

    def test_newinstance_stored_inobjects(self):
        self.assertIn(BaseModel(), models.storage.all().values())

    def test_id_ispublicstr(self):
        self.assertEqual(str, type(BaseModel().id))

    def test_created_at_ispublic_datetime(self):
        self.assertEqual(datetime, type(BaseModel().created_at))

    def test_updated_at_ispublic_datetime(self):
        self.assertEqual(datetime, type(BaseModel().updated_at))

    def test_twomodels_uniqueids(self):
        id1 = BaseModel()
        id2 = BaseModel()
        self.assertNotEqual(id1.id, id2.id)

    def test_twomodels_diff_created_at(self):
        b1 = BaseModel()
        sleep(0.5)
        b2 = BaseModel()
        self.assertLess(b1.created_at, b2.created_at)

    def test_twomodels_diff_updated_at(self):
        b1 = BaseModel()
        sleep(0.5)
        b2 = BaseModel()
        self.assertLess(b1.updated_at, b2.updated_at)

    def test_str_representation(self):
        t = datetime.now()
        trepr = repr(t)
        b = BaseModel()
        b.id = "129"
        b.created_at = b.updated_at = t
        bs = b.__str__()
        self.assertIn("[BaseModel] (129)", bs)
        self.assertIn("'id': '129'", bs)
        self.assertIn("'created_at': " + trepr, bs)
        self.assertIn("'updated_at': " + trepr, bs)

    def test_unused(self):
        b = BaseModel(None)
        self.assertNotIn(None, b.__dict__.values())

    def test_inst_with_kwargs(self):
        t = datetime.now()
        isot = t.isoformat()
        b = BaseModel(id="117", created_at=isot, updated_at=isot)
        self.assertEqual(b.id, "117")
        self.assertEqual(b.created_at, t)
        self.assertEqual(b.updated_at, t)

    def test_inst_with_No_kwargs(self):
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def test_inst_with_args_kwargs(self):
        t = datetime.now()
        isot = t.isoformat()
        b = BaseModel("20", id="125", created_at=isot, updated_at=isot)
        self.assertEqual(b.id, "125")
        self.assertEqual(b.created_at, t)
        self.assertEqual(b.updated_at, t)


class TestBaseModel_to_dict(unittest.TestCase):
    """to_dict method tests"""

    def test_to_dict_type(self):
        b = BaseModel()
        self.assertTrue(dict, type(b.to_dict()))

    def test_to_dict_correctkeys(self):
        b = BaseModel()
        self.assertIn("id", b.to_dict())
        self.assertIn("created_at", b.to_dict())
        self.assertIn("updated_at", b.to_dict())
        self.assertIn("__class__", b.to_dict())

    def test_to_dict_addattr(self):
        b = BaseModel()
        b.name = "Egypt"
        b.my_number = 89
        self.assertIn("name", b.to_dict())
        self.assertIn("my_number", b.to_dict())

    def test_to_dict_datetime_attr_strs(self):
        b = BaseModel()
        bdict = b.to_dict()
        self.assertEqual(str, type(bdict["created_at"]))
        self.assertEqual(str, type(bdict["updated_at"]))

    def test_to_dict_output(self):
        t = datetime.now()
        b = BaseModel()
        b.id = "678"
        b.created_at = b.updated_at = t
        bdict = {
            'id': '678',
            '__class__': 'BaseModel',
            'created_at': t.isoformat(),
            'updated_at': t.isoformat()
        }
        self.assertDictEqual(b.to_dict(), bdict)

    def test_contr_to_dict(self):
        b = BaseModel()
        self.assertNotEqual(b.to_dict(), b.__dict__)

    def test_to_dict_arg(self):
        b = BaseModel()
        with self.assertRaises(TypeError):
            b.to_dict(None)


class TestBaseModel_save(unittest.TestCase):
    """save method tests"""

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

    def test_onesave(self):
        b = BaseModel()
        sleep(0.11)
        fupdated_at = b.updated_at
        b.save()
        self.assertLess(fupdated_at, b.updated_at)

    def test_twsaves(self):
        b = BaseModel()
        sleep(0.1)
        fupdated_at = b.updated_at
        b.save()
        supdated_at = b.updated_at
        self.assertLess(fupdated_at, supdated_at)
        sleep(0.1)
        b.save()
        self.assertLess(supdated_at, b.updated_at)

    def test_save_arg(self):
        b = BaseModel()
        with self.assertRaises(TypeError):
            b.save(None)

    def test_save_updatefile(self):
        b = BaseModel()
        b.save()
        id1 = "BaseModel." + b.id
        with open("file.json", "r") as f:
            self.assertIn(id1, f.read())


if __name__ == "__main__":
    unittest.main()
