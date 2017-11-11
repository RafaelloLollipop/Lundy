import datetime
import hashlib
import importlib
import inspect
import json
import os
import pickle

import copy


def dumper(obj):
    try:
        return obj.toJSON()
    except:
        return obj.__dict__


class LundyObject():
    @property
    def hash(self):
        name_hash = hashlib.md5(self.name).hexdigest()
        obj_hash = hashlib.md5(self.to_string()).hexdigest()

        return name_hash + obj_hash

    def to_string(self):
        obj = self.to_json()
        return json.dumps(obj)


class LundyArg(LundyObject):
    type_mapping = {u"<type 'str'>": str,
                    u"<type 'NoneType'>": type(None),
                    u"<type 'int'>": int,
                    None: None}

    def __init__(self, name, default=None, type=None):
        self.name = name
        self.default = default
        self.type = type

    def to_json(self):
        obj = copy.copy(self)
        if self.type:
            obj.type = str(obj.type)
        return obj.__dict__

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    @classmethod
    def from_string(cls, str):
        json_from_str = json.loads(str)
        name = json_from_str['name']
        lundy_arg = LundyArg(name)

        arg_type = json_from_str['type']
        lundy_arg.type = LundyArg.type_mapping.get(arg_type)
        if lundy_arg.type:
            lundy_arg.default = json_from_str['default']
        return lundy_arg


class LundyMethod(LundyObject):
    def __init__(self, name):
        self.name = name
        self.args = []

    def scan(self, obj):
        if obj and type(obj) is not str:
            args = inspect.getargspec(obj).args
            defaults = inspect.getargspec(obj).defaults
            if not defaults:
                defaults = []
            for arg in args[:len(args) - len(defaults)]:
                lundy_arg = LundyArg(arg)
                self.args.append(lundy_arg)
            for arg, default in zip(args[len(args) - len(defaults):], defaults):
                lundy_arg = LundyArg(arg, default, type(default))
                self.args.append(lundy_arg)

    def to_json(self):
        obj = copy.copy(self)
        obj.args = []
        for arg in self.args:
            obj.args.append(arg.to_json())
        return obj.__dict__

    def __eq__(self, other):
        return all([arg for arg in self.args if arg in other.args]) and self.name == other.name

    @classmethod
    def from_string(cls, str):
        json_from_str = json.loads(str)
        name = json_from_str['name']
        args = []
        for arg in json_from_str['args']:
            lundy_arg = LundyArg.from_string(json.dumps(arg))
            args.append(lundy_arg)

        lundy_method = LundyMethod(name)
        lundy_method.args = args
        return lundy_method


class LundyClass(LundyObject):
    def __init__(self, name):
        self.name = name
        self.methods = []

    def scan(self, obj):
        for method_name, method_obj in inspect.getmembers(obj):
            lundy_method = LundyMethod(method_name)
            lundy_method.scan(method_obj)
            self.methods.append(lundy_method)

    def to_json(self):
        obj = copy.copy(self)
        obj.methods = []
        for method in self.methods:
            obj.methods.append(method.to_json())
        return obj.__dict__

    def __eq__(self, other):
        return all([method for method in self.methods if method in other.methods]) and self.name == other.name

    @classmethod
    def from_string(cls, str):
        json_from_str = json.loads(str)
        name = json_from_str['name']
        methods = []
        for method in json_from_str['methods']:
            lundy_method = LundyMethod.from_string(json.dumps(method))
            methods.append(lundy_method)

        lundy_class = LundyClass(name)
        lundy_class.methods = methods
        return lundy_class


class LundyModule(LundyObject):
    def __init__(self, py_path, os_path):
        self.py_path = py_path
        self.os_path = os_path
        self.classes = []

    def __repr__(self):
        return "[LundyModule] {}".format(self.py_path)

    def to_json(self):
        obj = copy.copy(self)
        obj.classes = []
        for cls in self.classes:
            obj.classes.append(cls.to_json())
        return obj.__dict__

    @property
    def hash(self):
        name_hash = hashlib.md5(self.py_path + self.os_path).hexdigest()
        obj_hash = hashlib.md5(self.to_string()).hexdigest()
        return name_hash + obj_hash

    def scan(self):
        module = importlib.import_module(self.py_path)
        for name, obj in inspect.getmembers(module, inspect.isclass):
            lundy_class = LundyClass(name)
            lundy_class.scan(obj)
            self.classes.append(lundy_class)

    def __eq__(self, other):
        return all([cls for cls in self.classes if cls in other.classes]) and self.py_path == other.py_path and self.os_path == other.os_path

    @classmethod
    def from_string(cls, str):
        json_from_str = json.loads(str)
        py_path = json_from_str['py_path']
        os_path = json_from_str['os_path']
        classes = []
        for class_string in json_from_str['classes']:
            lundy_class = LundyClass.from_string(json.dumps(class_string))
            classes.append(lundy_class)

        lundy_module = LundyModule(py_path, os_path)
        lundy_module.classes = classes
        return lundy_module


class LundyProject(LundyObject):
    MODULE_SEP = '.'

    def __init__(self, name):
        self.name = name
        self.modules = []

    def scan(self, src):
        for dirpath, dirnames, filenames in os.walk(src):
            if '__init__.py' not in filenames:
                continue
            for filename in filenames:
                if filename == '__init__.py' or filename.endswith('.pyc'):
                    continue
                full_module_path = os.path.join(dirpath, filename)
                base_path = os.path.dirname(src)
                os_module_path = os.path.relpath(full_module_path, base_path)
                project_module_path = os_module_path.replace(os.sep, self.MODULE_SEP).replace('.py', '')
                importlib.import_module(project_module_path)
                module = LundyModule(project_module_path, os_module_path)
                module.scan()
                self.modules.append(module)

    def to_json(self):
        obj = copy.copy(self)
        obj.modules = []
        for mod in self.modules:
            obj.modules.append(mod.to_json())
        return obj.__dict__

    def __eq__(self, other):
        return all([module for module in self.modules if module in other.modules]) and self.name == other.name

    @classmethod
    def from_string(cls, str):
        json_from_str = json.loads(str)
        name = json_from_str['name']
        modules = []
        for module in json_from_str['modules']:
            lundy_module = LundyModule.from_string(json.dumps(module))
            modules.append(lundy_module)

        lundy_project = LundyProject(name)
        lundy_project.modules = modules
        return lundy_project

class Method:
    def __init__(self, name, args, kwargs, result, hash):
        self.name = name
        self.args = args
        self.kwargs = kwargs
        self.result = result
        self.timestamp = datetime.datetime.now()
        self.hash = hash

    def save(self):
        pass
        # db = get_database()
        # print(db.lunni.insert({'abc': 2}))
        # print(db.instert(self))
        # coll.instert_one(self)
