import os
import urllib

from pymongo import MongoClient

dir_path = os.path.dirname(os.path.realpath(__file__))
def get_database():
    with open('../.lunni') as f:
        for line in f:
            command = line[:-1]
            command = command.split('=')
            if command[0] == 'uri':
                uri_path = command[1]
    uri_path = urllib.quote_plus(uri_path)
    #client = MongoClient(uri_path)

    user = urllib.quote("lunni")
    password = urllib.quote("afhJKH#$H@saC*&(")

    client = MongoClient("mongodb://{}:{}@192.166.218.144/lunni_test".format(user, password))
    db = client.lunni_test
    #print db.cool_collection.count()
    return db

def get_project_src():
    with open('../.lunni') as f:
        for line in f:
            command = line[:-1]
            command = command.split('=')

            if command[0] == 'project_source':
                project_src = command[1]
    user = urllib.quote("lunni")
    password = urllib.quote("afhJKH#$H@saC*&(")

    project_src = os.path.join(dir_path, project_src)
    return project_src