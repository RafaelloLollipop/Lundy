import datetime

from database import get_database


class Method:
    def __init__(self, name, args, kwargs, result):
        self.name = name
        self.args = args
        self.kwargs = kwargs
        self.result = result
        self.timestamp = datetime.datetime.now()

    def __repr__(self):
        return self.__dict__

    def save(self):
        db = get_database()
        print(db.lunni.insert({'abc': 2}))
        #print(db.instert(self))
        #coll.instert_one(self)