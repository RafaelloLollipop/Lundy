import importlib
import inspect
import os
import unittest
from types import NoneType

from app.datasets import LundyModule, LundyMethod, LundyClass, LundyArg, LundyProject
from app.test.sample_project_dir.sample_class import SampleClass

module = 'sample_project_dir.sample_class'
module = importlib.import_module(module)



EXPECTED_MODULES = [
    LundyModule('sample_project_dir.sample_class', 'sample_project_dir/sample_class.py'),
    LundyModule('sample_project_dir.sample_package.second_sample_class',
                'sample_project_dir/sample_package/second_sample_class.py'),
]

EXPECTED_CLASSES = ['SampleClass', 'SampleClass2']
EXPECTED_METHODS_NAMES = ['__doc__', '__init__', '__module__', 'sample_method', 'sample_method_with_args',
                          'sample_method_with_args_and_kwargs', 'sample_method_with_kwargs']
EXPECTED_METHODS = []
for method_name in EXPECTED_METHODS_NAMES:
    EXPECTED_METHODS.append(LundyMethod(method_name))


class LundyProjectTests(unittest.TestCase):
    def setUp(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        project_dir = os.path.join(dir_path, 'sample_project_dir')
        self.project = LundyProject("Lundy", project_dir)

    def test_find_all_modules_in_project(self):
        self.project.scan()
        self.assertEqual(len(self.project.modules), 2)
        for module, expected_module in zip(self.project.modules, EXPECTED_MODULES):
            self.assertEqual(module, expected_module)

    def test_to_json(self):
        self.project.scan()
        #self.project.to_json()

class LundyModuleTests(unittest.TestCase):
    def setUp(self):
        self.SAMPLE_PY_PATH = 'sample_project_dir.sample_class'
        self.SAMPLE_OS_PATH = 'sample_project_dir/sample_package/second_sample_class.py'
        print('')

    def test_scan_module(self):
        lundy_module = LundyModule(self.SAMPLE_PY_PATH, self.SAMPLE_OS_PATH)
        lundy_module.scan()
        self.assertEqual(len(lundy_module.classes), 2)
        self.assertEqual(len(lundy_module.classes[0].methods), 7)
        self.assertEqual(len(lundy_module.classes[1].methods), 2)

        for c in lundy_module.classes:
            self.assertIn(c.name, EXPECTED_CLASSES)
        for m in lundy_module.classes[0].methods:
            self.assertIn(m.name, EXPECTED_METHODS_NAMES)


class LundyClassTests(unittest.TestCase):
    def setUp(self):
        self.lundy_class = LundyClass('SampleClass')

    def test_scan(self):
        self.lundy_class.scan(SampleClass)
        self.assertEqual(self.lundy_class.name, 'SampleClass')
        self.assertEqual(len(self.lundy_class.methods), 7)
        for m in self.lundy_class.methods:
            self.assertIn(m.name, EXPECTED_METHODS_NAMES)


EXPECTED_ARGS = ['self', 'arg5', 'arg6', 'arg7', 'arg8']


class LundyMethodTests(unittest.TestCase):
    def setUp(self):
        self.lundy_method = LundyMethod('sample_method_with_args_and_kwargs')

    def test_scan(self):
        self.lundy_method.scan(SampleClass.sample_method_with_args_and_kwargs)
        self.assertEqual(len(self.lundy_method.args), 5)
        EXPECTED_ARGS_WITH_DEFAULT = 2
        default = 0
        for arg in self.lundy_method.args:
            self.assertIn(arg.name, EXPECTED_ARGS)
            if arg.type:
                default += 1
        self.assertEqual(default, EXPECTED_ARGS_WITH_DEFAULT)

    def test_json(self):
        self.lundy_method.scan(SampleClass.sample_method_with_args_and_kwargs)
        EXPECTED_JSON = {'args': [{'default': None, 'type': None, 'name': 'self'}, {'default': None, 'type': None, 'name': 'arg5'}, {'default': None, 'type': None, 'name': 'arg6'}, {'default': None, 'type': "<type 'NoneType'>", 'name': 'arg7'}, {'default': 4, 'type': "<type 'int'>", 'name': 'arg8'}], 'name': 'sample_method_with_args_and_kwargs'}
        json_from_method = self.lundy_method.to_json()
        self.assertEqual(json_from_method, EXPECTED_JSON)
        self.assertEqual(type(json_from_method), dict)
        EXPECTED_STRING = '''{"args": [{"default": null, "type": null, "name": "self"}, {"default": null, "type": null, "name": "arg5"}, {"default": null, "type": null, "name": "arg6"}, {"default": null, "type": "<type 'NoneType'>", "name": "arg7"}, {"default": 4, "type": "<type 'int'>", "name": "arg8"}], "name": "sample_method_with_args_and_kwargs"}'''
        string_from_method = self.lundy_method.to_string()
        self.assertEqual(string_from_method, EXPECTED_STRING)
        self.assertEqual(type(string_from_method), str)


class LundyArgTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_arg(self):
        lundy_arg = LundyArg('name')
        lundy_arg.name = 'name'

    def test_default_arg(self):
        lundy_arg = LundyArg('name', 'Rafal', type=type('Rafal'))
        self.assertEqual(lundy_arg.name, 'name')
        self.assertEqual(lundy_arg.default, 'Rafal')
        self.assertEqual(lundy_arg.type, str)

    def test_none_as_default_arg(self):
        lundy_arg = LundyArg('name', None, type=type(None))
        self.assertEqual(lundy_arg.name, 'name')
        self.assertEqual(lundy_arg.default, None)
        self.assertEqual(lundy_arg.type, NoneType)

    def test_hash(self):
        EXPECTED_HASH = 'b068931cc450442b63f5b3d276ea4297766d2bc97441bdf27faaabad3ff3564e'
        lundy_arg = LundyArg('name')
        self.assertEqual(lundy_arg.hash, EXPECTED_HASH)

        EXPECTED_HASH = 'b068931cc450442b63f5b3d276ea429707be451fb71438ab1e088bd3dea1f194'
        lundy_arg = LundyArg('name', 'Rafal', type=type('Rafal'))
        self.assertEqual(lundy_arg.hash, EXPECTED_HASH)

        EXPECTED_HASH = 'b068931cc450442b63f5b3d276ea42976d6a4895bdde068275009cefc4a80d9f'
        lundy_arg = LundyArg('name', None, type=type(None))
        self.assertEqual(lundy_arg.hash, EXPECTED_HASH)

    def test_to_json(self):
        lundy_arg = LundyArg('name')
        EXPECTED_JSON = {'default': None, 'type': None, 'name': 'name'}
        json_from_arg = lundy_arg.to_json()
        self.assertEqual(json_from_arg, EXPECTED_JSON)
        self.assertEqual(type(json_from_arg), dict)

        EXPECTED_STRING = '''{"default": null, "type": null, "name": "name"}'''
        string_from_arg = lundy_arg.to_string()
        self.assertEqual(string_from_arg, EXPECTED_STRING)
        self.assertEqual(type(string_from_arg), str)

        lundy_arg = LundyArg('name', 'Rafal', type=type('Rafal'))
        EXPECTED_JSON = {'default': 'Rafal', 'type': "<type 'str'>", 'name': 'name'}
        json_from_arg = lundy_arg.to_json()
        self.assertEqual(json_from_arg, EXPECTED_JSON)
        self.assertEqual(type(json_from_arg), dict)

        EXPECTED_STRING = '''{"default": "Rafal", "type": "<type 'str'>", "name": "name"}'''
        string_from_arg = lundy_arg.to_string()
        self.assertEqual(string_from_arg, EXPECTED_STRING)
        self.assertEqual(type(string_from_arg), str)

        lundy_arg = LundyArg('name', None, type=type(None))
        EXPECTED_JSON = {'default': None, 'type': "<type 'NoneType'>", 'name': 'name'}
        json_from_arg = lundy_arg.to_json()
        self.assertEqual(json_from_arg, EXPECTED_JSON)
        self.assertEqual(type(json_from_arg), dict)

        EXPECTED_STRING = '''{"default": null, "type": "<type 'NoneType'>", "name": "name"}'''
        string_from_arg = lundy_arg.to_string()
        self.assertEqual(string_from_arg, EXPECTED_STRING)
        self.assertEqual(type(string_from_arg), str)