import unittest
from mock import patch

import mongomock as mongomock

from lundy.datasets import LundyObject, LundyModule, ResultPackage
from lundy.test.sample_project_dir.sample_class import SampleClass
from main import Lundy


class BasicMethodTests(unittest.TestCase):
    def setUp(self):
        pass

    @patch('lundy.datasets.get_database')
    def test_send_method_result(self, get_database_patch):
        lunni_collection = mongomock.MongoClient().db.lunni_test
        get_database_patch.return_value = lunni_collection
        test_method = ["test", ['1'], ['2'], ['3'], 'adsa', 3, 3]
        m = ResultPackage(*test_method)
        m.save()



class BasicCollectTests(unittest.TestCase):
    def setUp(self):
        pass

    @patch('datasets.get_database')
    def test_collect_sample_class(self, get_database_patch):
        lunni_collection = mongomock.MongoClient().db.lunni_test
        get_database_patch.return_value = lunni_collection
        sample_class = Lundy.collector()
        sample_class(SampleClass)
        sample_class = SampleClass('rafal', 'pafal')
        sample_class.sample_method()
        sample_class.sample_method_with_args("A", "B")
        sample_class.sample_method_with_args_and_kwargs("Y", "W")
        sample_class.sample_method_with_kwargs()
        lunni_collection.find_one()

    @patch('datasets.get_database')
    def test_random(self, get_database_patch):
        lunni_collection = mongomock.MongoClient().db.lunni_test
        get_database_patch.return_value = lunni_collection
        self.SAMPLE_PY_PATH = 'sample_project_dir.sample_class'
        self.SAMPLE_OS_PATH = 'sample_project_dir/sample_package/second_sample_class.py'
        self.lundy_module = LundyModule(self.SAMPLE_PY_PATH, self.SAMPLE_OS_PATH)
        self.lundy_module.scan()

        sample_class = SampleClass('rafal', 'pafal')
        sample_class2 = SampleClass(sample_class, 'pafal')
        sample_class2.sample_method_with_args(sample_class, "B")

    def run_method_once_again(self):
        import datetime
        data = {'hash': '19479db44a6d5584037ee303531f7b25c4f799327c8fb73cf30dc8874622c54c', 'name': 'sample_method_with_args', 'kwargs': {}, 'duration': 6e-06, 'timestamp': datetime.datetime(2017, 11, 17, 17, 38, 59, 270600), 'args': ({'var1': 'var1', 'var3': 'pafal', 'var2': 'rafal'}, 'A', 'B'), 'result': ('A', 'B')}
        class FakeSelf():
            pass
        fake_self = FakeSelf
        for key, value in data['args'][0].items():
            setattr(fake_self, key, value)
        self.assertEqual(data['result'], SampleClass.__dict__['sample_method_with_args'](fake_self, data['args'][1], data['args'][2]))
